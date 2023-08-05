"""mse_cli_core.no_sgx_docker module."""

from pathlib import Path
from typing import ClassVar, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from mse_cli_core.sgx_docker import SgxDockerConfig


class NoSgxDockerConfig(BaseModel):
    """Definition of an mse docker running on a non-sgx hardware."""

    host: str
    expiration_date: Optional[int]
    app_cert: Optional[Path]
    size: int
    app_id: UUID
    application: str

    code_mountpoint: ClassVar[str] = "/tmp/app.tar"
    app_cert_mountpoint: ClassVar[str] = "/tmp/cert.pem"
    entrypoint: ClassVar[str] = "mse-run"

    def cmd(self) -> List[str]:
        """Serialize the docker command args."""
        command = [
            "--size",
            f"{self.size}M",
            "--code",
            NoSgxDockerConfig.code_mountpoint,
            "--san",
            str(self.host),
            "--id",
            str(self.app_id),
            "--application",
            self.application,
            "--dry-run",
        ]

        if self.app_cert:
            command.append("--certificate")
            command.append(NoSgxDockerConfig.app_cert_mountpoint)
        else:
            command.append("--ratls")
            command.append(str(self.expiration_date))

        return command

    def volumes(self, code_tar_path: Path) -> Dict[str, Dict[str, str]]:
        """Define the docker volumes."""
        v = {
            f"{code_tar_path.resolve()}": {
                "bind": NoSgxDockerConfig.code_mountpoint,
                "mode": "rw",
            }
        }

        if self.app_cert:
            v[f"{self.app_cert.resolve()}"] = {
                "bind": NoSgxDockerConfig.app_cert_mountpoint,
                "mode": "rw",
            }

        return v

    @staticmethod
    def from_sgx(docker_config: SgxDockerConfig):
        """Load from a SgxDockerConfig object."""
        return NoSgxDockerConfig(
            host=docker_config.host,
            expiration_date=docker_config.expiration_date,
            size=docker_config.size,
            app_id=docker_config.app_id,
            application=docker_config.application,
        )
