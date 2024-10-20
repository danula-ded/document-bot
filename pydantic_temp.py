from dataclasses import dataclass

from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int


class User2(BaseModel):
    name: str
    age: int
    user: User


@dataclass
class UserDTO:
    name: str
    age: int


if __name__ == '__main__':
    a = User(name='asda', age='123')
    x = User2(name='asda', age='123', user=a)
