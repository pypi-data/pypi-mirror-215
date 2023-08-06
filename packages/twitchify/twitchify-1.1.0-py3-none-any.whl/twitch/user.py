"""
The MIT License (MIT)

Copyright (c) 2023-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from .utils import parse_rfc3339_timestamp

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub import (channel as chl, user as us)
    from typing import Optional, Dict, Any
    from datetime import datetime


class User:
    """
    Represents a user.
    """
    __slots__ = ('id', 'name', 'display_name')

    def __init__(self, *, user: Dict[str, Any], prefix: str = 'user') -> None:
        self.id: str = user.get(f'{prefix}_id') or '0'
        self.name: str = user.get(f'{prefix}_login') or 'anonymous'
        self.display_name: str = user.get(f'{prefix}_name') or 'Anonymous'

    def __repr__(self) -> str:
        return f'<User id={self.id} login={self.name} display_name={self.display_name}>'


class Follower(User):
    """
    Represents a follower user.
    """
    __slots__ = ('followed_at',)

    def __init__(self, *, channel: chl.Follow) -> None:
        super().__init__(user=channel)
        self.followed_at: datetime = parse_rfc3339_timestamp(timestamp=channel['followed_at'])

    def __repr__(self) -> str:
        return f'<Follower {super().__repr__()} followed_at={self.followed_at}>'


class UserUpdate(User):
    """
    Represents a user who has updated their information.
    """
    __slots__ = ('description', 'email', 'email_verified')

    def __init__(self, *, update: us.Update) -> None:
        super().__init__(user=update)
        self.description: str = update['description']
        self.email: Optional[str] = update.get('email')  # Requires user:read:email scope
        self.email_verified: bool = update['email_verified']

    def __repr__(self) -> str:
        return f'<Update user={super().__repr__()} description={self.description}>'
