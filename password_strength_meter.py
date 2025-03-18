import streamlit as st
import re
import secrets
import string

BLACKLIST = [
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "abc123",
    "letmein",
    "admin",
]
UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SPECIALS = "!@#$%^&*"
ALLOWED_CHARACTERS = UPPERCASE + LOWERCASE + DIGITS + SPECIALS


def evaluate_password(password: str) -> tuple[int, str, list[str]]:
    score: int = 0
    feedback: list[str] = []

    if password.lower() in BLACKLIST:
        feedback.append(
            "❌ This password is too common. Please choose a more unique password."
        )
        return 1, "Blacklisted", feedback

    if len(password) >= 8:
        score += 2
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    if score <= 2:
        strength_msg = "❌ Weak Password - Improve it using the suggestions below."
    elif score == 3:
        strength_msg = "⚠️ Moderate Password - Consider adding more security features."
    else:
        strength_msg = "✅ Strong Password!"

    return score, strength_msg, feedback


def generate_strong_password(length: int) -> str:
    return "".join(secrets.choice(ALLOWED_CHARACTERS) for _ in range(length))


def main() -> None:
    st.title("Password Strength Meter & Generator")
    st.write(
        "Check the strength of your password or generate a strong password suggestion."
    )
    option = st.selectbox(
        "Choose an option:", ["Check Password Strength", "Generate Strong Password"]
    )

    if option == "Check Password Strength":
        user_password = st.text_input("Enter your password:", type="password")
        if user_password:
            try:
                score, strength_msg, feedback = evaluate_password(user_password)
                st.markdown("### Password Evaluation")
                st.write(strength_msg)
                st.write(f"**Score:** {score}/5")
                if feedback:
                    st.subheader("Suggestions:")
                    for tip in feedback:
                        st.write(tip)
            except Exception as e:
                st.error(f"An error occurred while evaluating the password: {e}")

    elif option == "Generate Strong Password":
        length = st.slider(
            "Select password length:", min_value=8, max_value=20, value=12
        )
        if st.button("Generate Password"):
            try:
                new_password = generate_strong_password(length)
                st.markdown("### Generated Password")
                st.code(new_password)
            except Exception as e:
                st.error(f"An error occurred while generating the password: {e}")


if __name__ == "__main__":
    main()
