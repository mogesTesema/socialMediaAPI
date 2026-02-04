from foodapp.core.config import config
import httpx
from fastapi import HTTPException


async def send_verfication_email(to: str, token: str, verify_url: str):
    payload = {
        "sender": {"email": config.BREVO_SENDER},
        "to": [{"email": to}],
        "subject": "Verify your email",
        "htmlContent": f"""
            <p>Click the link below to verify your email:</p>
            <a href="{verify_url}">Verify Email</a>
            <p>If you didn't create an account, ignore this email.</p>
        """,
    }

    headers = {
        "api-key": config.BREVO_API_KEY,
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.brevo.com/v3/smtp/email",
                headers=headers,
                json=payload,
                timeout=20.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Brevo email varification failed:{e}",
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="internal server error durring sending email confirmation",
            )
        return response.json()


async def send_password_reset_email(to: str, reset_url: str):
    payload = {
        "sender": {"email": config.BREVO_SENDER},
        "to": [{"email": to}],
        "subject": "Reset your password",
        "htmlContent": f"""
            <p>Click the link below to reset your password:</p>
            <a href="{reset_url}">Reset Password</a>
            <p>If you didn't request a reset, you can ignore this email.</p>
        """,
    }

    headers = {
        "api-key": config.BREVO_API_KEY,
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.brevo.com/v3/smtp/email",
                headers=headers,
                json=payload,
                timeout=20.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Brevo password reset email failed:{e}",
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="internal server error during sending password reset email",
            )
        return response.json()
