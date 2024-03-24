from quick_sqlite import Database
from dotenv import load_dotenv

from typing import Any

load_dotenv()

class BotDatabase(Database):
    def __init__(self, path: str, db_name: str = "__default__", auto_init: Any = None) -> None:
        super().__init__(path, db_name, auto_init)

    def __str__(self) -> str:
        all = super().get_all()
        
        output = [f"    {item.key}: {item.value}" for item in all]
        
        return '{\n' + '\n'.join(output) + '\n}'

    def get(self, key, default=None) -> Any:
        return default if not super().get(key) else super().get(key)

    def add(self, key, more:int):
        return super().append(key, more)

    def append(self, key, more) -> Any:

        data: list = self.get(key, [])
        data.append(more)
                
        return self.set(key, data)

    def remove(self, key, id) -> Any:
        data: list = self.get(key, [])
        data.remove(id)
        self.set(key, data)
        if id in data:
            return self.remove(key, id)
        
if __name__ == "__main__":
    db = BotDatabase('bot.db')
    print(db)