
import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from game_data import games
from nlp_engine import get_similarity, get_feedback, get_smart_hint
from database import create_database, save_score, get_leaderboard

# -----------------------------
# Database and page setup
# -----------------------------

create_database()

st.set_page_config(
    page_title="MindMaze",
    page_icon="🧩",
    layout="centered"
)

TIME_LIMITS = {
    "Easy": 60,
    "Medium": 45,
    "Hard": 30
}

# -----------------------------
# Session state
# -----------------------------

defaults = {
    "page": "welcome",
    "difficulty": "Easy",
    "level": 0,
    "score": 0,
    "solved": False,
    "hint": False,
    "feedback": "",
    "similarity": None,
    "player_name": "",
    "score_saved": False,
    "room_started_at": None,
    "time_up": False,
    "last_points": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def start_game():
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.solved = False
    st.session_state.hint = False
    st.session_state.feedback = ""
    st.session_state.similarity = None
    st.session_state.score_saved = False
    st.session_state.time_up = False
    st.session_state.last_points = 0
    st.session_state.room_started_at = time.time()
    st.session_state.page = "game"


def next_room():
    st.session_state.level += 1
    st.session_state.solved = False
    st.session_state.hint = False
    st.session_state.feedback = ""
    st.session_state.similarity = None
    st.session_state.time_up = False
    st.session_state.last_points = 0

    questions = games[st.session_state.difficulty]

    if st.session_state.level >= len(questions):
        st.session_state.page = "complete"
        st.session_state.room_started_at = None
    else:
        st.session_state.room_started_at = time.time()


# -----------------------------
# Welcome page
# -----------------------------

if st.session_state.page == "welcome":

    st.title("🧩 MindMaze")
    st.subheader("The Semantic Word Escape Game")

    st.write(
        "Enter the virtual maze, solve word puzzles, "
        "and escape using your NLP skills!"
    )

    name = st.text_input(
        "Enter your player name",
        value=st.session_state.player_name
    )
    st.session_state.player_name = name.strip()

    difficulty = st.selectbox(
        "Choose your difficulty",
        ["Easy", "Medium", "Hard"]
    )
    st.session_state.difficulty = difficulty

    st.info(
        f"⏱️ Time per room: {TIME_LIMITS[difficulty]} seconds"
    )

    if st.button("🚀 Start Game", use_container_width=True):
        if not st.session_state.player_name:
            st.warning("Please enter your name first!")
        else:
            start_game()
            st.rerun()

    st.divider()

    st.subheader("📖 How to Play")
    st.write("1. Read the clue and guess the hidden word.")
    st.write("2. The NLP model checks the meaning of your answer.")
    st.write("3. Get closer to the target word to receive feedback.")
    st.write("4. Use hints carefully because they reduce your points.")
    st.write("5. Solve all three rooms before time runs out!")

    st.caption(
        "Scoring: 10 base points + up to 5 time bonus points. "
        "Using a hint costs 2 points."
    )


# -----------------------------
# Game page
# -----------------------------

elif st.session_state.page == "game":

    questions = games[st.session_state.difficulty]
    level = st.session_state.level

    target, clue, fallback_hint = questions[level]
    time_limit = TIME_LIMITS[st.session_state.difficulty]

    # Refresh the page every second while playing
    if not st.session_state.solved and not st.session_state.time_up:
        st_autorefresh(
            interval=1000,
            key=f"timer_room_{level}"
        )

    elapsed = int(time.time() - st.session_state.room_started_at)
    remaining = max(0, time_limit - elapsed)

    if remaining <= 0 and not st.session_state.solved:
        st.session_state.time_up = True

    st.title("🧩 MindMaze")
    st.write(f"Welcome, **{st.session_state.player_name}**!")

    st.progress((level + 1) / len(questions))
    st.subheader(
        f"🚪 Room {level + 1} of {len(questions)}"
    )

    st.write(f"**Difficulty:** {st.session_state.difficulty}")
    st.write(f"**Current Score:** {st.session_state.score}")

    # Countdown timer
    if not st.session_state.solved and not st.session_state.time_up:
        st.metric("⏱️ Time Remaining", f"{remaining} seconds")

        if remaining <= 10:
            st.warning("Hurry up! Time is running out!")

    st.divider()

    st.subheader("🔍 Find the Hidden Word")
    st.info(clue)

    # Answer form
    if not st.session_state.solved and not st.session_state.time_up:

        with st.form("answer_form"):
            answer = st.text_input("Enter your guess")
            submitted = st.form_submit_button("Submit Answer")

        if submitted:

            if not answer.strip():
                st.warning("Please enter a word!")
            else:
                # Check time again when answer is submitted
                elapsed = int(
                    time.time() - st.session_state.room_started_at
                )
                remaining = max(0, time_limit - elapsed)

                if remaining <= 0:
                    st.session_state.time_up = True
                    st.rerun()

                similarity = get_similarity(answer, target)
                st.session_state.similarity = similarity

                if answer.strip().lower() == target.lower():
                    bonus = 5 if remaining <= 10 else (
                        3 if remaining <= 20 else 0
                    )

                    penalty = 2 if st.session_state.hint else 0
                    points = max(0, 10 + bonus - penalty)

                    st.session_state.score += points
                    st.session_state.last_points = points
                    st.session_state.solved = True

                    st.session_state.feedback = (
                        f"🎉 Correct! You earned {points} points!"
                    )

                else:
                    st.session_state.feedback = get_feedback(similarity)

                st.rerun()

        # Smart hint
        if st.button("💡 Get Smart Hint"):
            st.session_state.hint = True
            st.rerun()

        if st.session_state.hint:
            st.warning(
                get_smart_hint(target, fallback_hint)
            )
            st.caption("Using a hint costs 2 points.")

    # NLP feedback
    if st.session_state.feedback:
        st.write(st.session_state.feedback)

        if st.session_state.similarity is not None:
            st.write(
                f"Semantic similarity: "
                f"{st.session_state.similarity:.2f}"
            )

    # Correct answer
    if st.session_state.solved:
        st.success("🔓 Room unlocked!")
        st.write(f"Points earned in this room: {st.session_state.last_points}")

        if st.button("➡️ Next Room", use_container_width=True):
            next_room()
            st.rerun()

    # Time up
    if st.session_state.time_up:
        st.error("⏰ Time's up!")
        st.write(f"The correct answer was: **{target}**")
        st.write("You earned 0 points in this room.")

        if st.button("➡️ Continue to Next Room", use_container_width=True):
            next_room()
            st.rerun()


# -----------------------------
# Completion page
# -----------------------------

elif st.session_state.page == "complete":

    st.title("🏆 Maze Completed!")
    st.balloons()

    st.success(
        f"Congratulations, {st.session_state.player_name}!"
    )

    total_possible = len(
        games[st.session_state.difficulty]
    ) * 15

    st.metric(
        "Your Final Score",
        f"{st.session_state.score} / {total_possible}"
    )

    if not st.session_state.score_saved:
        save_score(
            st.session_state.player_name,
            st.session_state.difficulty,
            st.session_state.score
        )
        st.session_state.score_saved = True

    st.divider()

    st.subheader("🏅 Leaderboard")

    leaderboard = get_leaderboard()

    if leaderboard:
        st.table([
            {
                "Player": row[0],
                "Difficulty": row[1],
                "Score": row[2]
            }
            for row in leaderboard
        ])
    else:
        st.write("No scores available yet.")

    if st.button("🔄 Play Again", use_container_width=True):
        start_game()
        st.rerun()

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.page = "welcome"
        st.rerun()
