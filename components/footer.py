import streamlit as st

def display_footer():
    """
    Display a consistent footer across all pages that matches the design shown in the image.
    """
    
    # Footer HTML structure
    st.markdown("""
    <div class="footer-container">
        <div class="logo-container">
            <img src="app/static/images/palayan-logo-png.png" alt="Palayan Logo">
            <img src="app/static/images/ph-gov.png" alt="Bagon Pilipinas Logo">
        </div>
        <div class="footer-title">TALK TO PALAYAN</div>
        <div class="footer-subtitle">City Citizen Feedback Hub</div>
        <div class="footer-copyright">© Palayan City | TALK TO PALAYAN | All Rights Reserved</div>
    </div>
    """, unsafe_allow_html=True)