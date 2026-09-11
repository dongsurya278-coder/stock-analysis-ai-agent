"""Tests for data fetchers"""
import pytest
from app.data.iex_client import IEXCloudClient
from app.data.yahoo_client import YahooFinanceClient


def test_iex_client_init():
    """Test IEX client initialization"""
    client = IEXCloudClient()
    assert client is not None


def test_yahoo_client_init():
    """Test Yahoo Finance client initialization"""
    client = YahooFinanceClient()
    assert client is not None
