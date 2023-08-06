"""Characters"""

from typing import Optional, Sequence

from attrs import define

__all__: Sequence[str] = ("Character",)


@define
class Character:
    """*Character*

    # Fields

    * `weight` - ...
    * `name` - ...
    * `description` - ...

    # Examples
    ```
    from gacha import Character
    ...
    Character(0.003, name="Jean", description="https://genshin-impact.fandom.com/wiki/Jean")
    Character(0.003, name="Qiqi", description="https://genshin-impact.fandom.com/wiki/Qiqi")
    Character(0.003, name="Tighnari", description="https://genshin-impact.fandom.com/wiki/Tighnari")
    Character(0.003, name="Keqing", description="https://genshin-impact.fandom.com/wiki/Keqing")
    Character(0.003, name="Mona", description="https://genshin-impact.fandom.com/wiki/Mona")
    Character(0.003, name="Dehya", description="https://genshin-impact.fandom.com/wiki/Dehya")
    Character(0.003, name="Diluc", description="https://genshin-impact.fandom.com/wiki/Diluc")
    ...
    ```
    """

    weight: float

    name: Optional[str] = None
    description: Optional[str] = None
