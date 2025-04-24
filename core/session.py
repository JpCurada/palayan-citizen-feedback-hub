import streamlit as st

class SessionManager:
    """Class to manage Streamlit session state."""

    def __init__(self, defaults=None):
        if defaults is None:
            defaults = {}
        self.defaults = defaults
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state with default values."""
        for key, default_value in self.defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def reset(self, keys):
        """Reset specific session state keys to their default values."""
        for key in keys:
            if key in self.defaults:
                st.session_state[key] = self.defaults[key]

    def set(self, key, value):
        """Set a session state key to a specific value."""
        st.session_state[key] = value

    def get(self, key, default=None):
        """Get a session state key value, with an optional default."""
        return st.session_state.get(key, default) 