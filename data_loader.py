

from typing import Generator, List
from dataclasses import dataclass

@dataclass
class FastaRecord:
    id: str
    desc: str
    seq: str

def parse_fasta(path: str) -> Generator[FastaRecord, None, None]:
    header = None
    seq_chunks: List[str] = []

    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            if line.startswith('>'):
                if header is not None:
                    rec_id, desc = header.split(None, 1) if ' ' in header else (header, '')
                    yield FastaRecord(rec_id, desc, ''.join(seq_chunks))
                header = line[1:]
                seq_chunks = []
            else:
                seq_chunks.append(line)
        if header is not None:
            rec_id, desc = header.split(None, 1) if ' ' in header else (header, '')
            yield FastaRecord(rec_id, desc, ''.join(seq_chunks))



