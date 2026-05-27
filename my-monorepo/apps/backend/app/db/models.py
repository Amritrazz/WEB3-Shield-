from sqlalchemy import Column, String, Float, Boolean, DateTime, Text, JSON, UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

class ThreatReport(Base):
    __tablename__ = "threat_reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)   # phishing_url | scam_wallet | malicious_contract
    target = Column(String, nullable=False)
    ai_score = Column(Float)
    flags = Column(JSON)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = Column(String, unique=True, nullable=False)
    chain = Column(String, nullable=False)
    risk_score = Column(Float, default=0)
    label = Column(String, default="unknown")
    updated_at = Column(DateTime, default=datetime.utcnow)