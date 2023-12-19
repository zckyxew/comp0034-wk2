# Adapted from https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#define-models
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from paralympics import db
import bcrypt


# This uses the latest syntax for SQLAlchemy, older tutorials will show different syntax
# SQLAlchemy provide an __init__ method for each model, so you do not need to declare this in your code
class Region(db.Model):
    __tablename__ = "region"
    NOC: Mapped[str] = mapped_column(db.Text, primary_key=True)
    region: Mapped[str] = mapped_column(db.Text, nullable=False)
    notes: Mapped[str] = mapped_column(db.Text, nullable=True)
    # one-to-many relationship with Event https: // docs.sqlalchemy.org / en / 20 / orm / basic_relationships.html
    events: Mapped[list["Event"]] = relationship(back_populates="region")


class Event(db.Model):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    type: Mapped[str] = mapped_column(db.Text, nullable=False)
    year: Mapped[int] = mapped_column(db.Integer, nullable=False)
    country: Mapped[str] = mapped_column(db.Text, nullable=False)
    host: Mapped[str] = mapped_column(db.Text, nullable=False)
    # add ForeignKey to mapped_column(String, primary_key=True)
    NOC: Mapped[str] = mapped_column(ForeignKey("region.NOC"))
    # add relationship to mapped_column(String, primary_key=True)
    region: Mapped[Region] = relationship("Region", back_populates="events")
    start: Mapped[str] = mapped_column(db.Text, nullable=True)
    end: Mapped[str] = mapped_column(db.Text, nullable=True)
    duration: Mapped[int] = mapped_column(db.Integer, nullable=True)
    disabilities_included: Mapped[str] = mapped_column(db.Text, nullable=True)
    countries: Mapped[str] = mapped_column(db.Text, nullable=True)
    events: Mapped[int] = mapped_column(db.Integer, nullable=True)
    athletes: Mapped[int] = mapped_column(db.Integer, nullable=True)
    sports: Mapped[int] = mapped_column(db.Integer, nullable=True)
    participants_m: Mapped[int] = mapped_column(db.Integer, nullable=True)
    participants_f: Mapped[int] = mapped_column(db.Integer, nullable=True)
    participants: Mapped[int] = mapped_column(db.Integer, nullable=True)
    highlights: Mapped[str] = mapped_column(db.Integer, nullable=True)


class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)

    def __init__(self, email: str, password_string: str):
        """
        Create a new User object using hashing the plain text password.
        :type password_string: str
        :type email: str
        :returns None
        """
        self.email = email
        self.password = self._hash_password(password_string)

    def __repr__(self):
        """
        Returns the attributes of a User as a string, except for the password
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.id}, {self.email}>"

    @staticmethod
    def _hash_password(password_string: str):
        """Hash a password using bcrypt"""  # https://pypi.org/project/bcrypt/
        # bcrypt requires a byte string, so encode the password
        password = password_string.encode('utf-8')
        # generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password

    def set_password(self, password_string: str):
        """Set a new password for the user"""
        self.password = self._hash_password(password_string)

    def verify_password(self, password_string: str):
        """ Verify a password against the stored hash"""
        # bcrypt requires a byte string, so encode the password
        password_b = password_string.encode('utf-8')
        # verify the password against the stored hash
        return bcrypt.checkpw(password_b, self.password)
