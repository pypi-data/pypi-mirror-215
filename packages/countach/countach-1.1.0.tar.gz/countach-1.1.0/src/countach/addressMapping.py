from dataclasses import dataclass

@dataclass
class AddressMapping:
	originalAddress: int
	mappingAddress: int
	length: int
