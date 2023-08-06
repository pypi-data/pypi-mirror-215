"""mse_cli_core.enclave module."""

import re
from pathlib import Path
from typing import Optional, Tuple, Union

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.x509 import Certificate, CertificateRevocationList
from docker.client import DockerClient
from intel_sgx_ra.attest import verify_quote
from intel_sgx_ra.ratls import ratls_verify
from intel_sgx_ra.signer import mr_signer_from_pk

from mse_cli_core.no_sgx_docker import NoSgxDockerConfig


class WrongMREnclave(Exception):
    """MR enclave does not matched with the expected value."""


class WrongMRSigner(Exception):
    """MR signer does not matched with the expected value."""


def compute_mr_enclave(
    client: DockerClient,
    image: str,
    app_args: NoSgxDockerConfig,
    app_path: Path,
    docker_path_log: Path,
) -> str:
    """Compute the MR enclave."""
    container = client.containers.run(
        image,
        command=app_args.cmd(),
        volumes=app_args.volumes(app_path),
        entrypoint=NoSgxDockerConfig.entrypoint,
        remove=True,
        detach=False,
        stdout=True,
        stderr=True,
    )

    # Save the docker output
    docker_path_log.write_bytes(container)

    # Get the mr_enclave from the docker output
    pattern = "Measurement:\n[ ]*([a-z0-9]{64})"
    m = re.search(pattern.encode("utf-8"), container)

    if not m:
        raise Exception(
            f"Fail to compute mr_enclave! See {docker_path_log} for more details."
        )

    return str(m.group(1).decode("utf-8"))


def verify_enclave(
    signer_pk: Union[RSAPublicKey, Path, bytes],
    ratls_certificate: Union[str, bytes, Path, Certificate],
    fingerprint: Optional[str],
    collaterals: Optional[
        Tuple[
            bytes,
            bytes,
            Certificate,
            CertificateRevocationList,
            CertificateRevocationList,
        ]
    ] = None,
    pccs_url: Optional[str] = None,
):
    """Verify an enclave trustworthiness."""
    # Compute MRSIGNER value from public key
    mrsigner = mr_signer_from_pk(signer_pk)

    # Check certificate's public key in quote's user report data
    quote = ratls_verify(ratls_certificate)

    # Check MRSIGNER
    if quote.report_body.mr_signer != mrsigner:
        raise WrongMRSigner(
            "Enclave signer is wrong "
            f"(read {bytes(quote.report_body.mr_signer).hex()} "
            f"but should be {bytes(mrsigner).hex()})"
        )

    # Check enclave certificates and information
    verify_quote(quote=quote, collaterals=collaterals, pccs_url=pccs_url)

    # Check MRENCLAVE
    if fingerprint:
        if quote.report_body.mr_enclave != bytes.fromhex(fingerprint):
            raise WrongMREnclave(
                "Code fingerprint is wrong "
                f"(read {bytes(quote.report_body.mr_enclave).hex()} "
                f"but should be {fingerprint})"
            )
