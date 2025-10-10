class UserFiles(Base):
    __tablename__ = "user_files"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True
    )
    file_id = Column(
        UUID(as_uuid=True),
        primary_key=True
    )

    user = relationship(
        "User",
        back_populates="user_files",
        foreign_keys=[user_id],
        lazy="select"
    )

    file = relationship(
        "File",
        back_populates="user_files",
        foreign_keys=[file_id],
        lazy="select"
    )

    def __init__(self, user=None, file=None):
        if user is not None:
            self.user = user
        if file is not None:
            self.file = file

    @property
    def id(self):
        return (self.user_id, self.file_id)

    @property
    def get_user(self):
        return self.user

    @property
    def get_file(self):
        return self.file

    def __repr__(self):
        return f"UserFiles(user_id={self.user_id}, file_id={self.file_id})"