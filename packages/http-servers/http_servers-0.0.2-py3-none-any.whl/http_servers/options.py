from dataclasses import dataclass


@dataclass
class ServerOptions:
    cors: bool
    host: str
    port: int
    cache: bool
    source_dir: str
