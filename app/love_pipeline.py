import streamlit as st
import time
import os
import base64
import datetime
from io import BytesIO
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# --- Page Config ---
st.set_page_config(page_title="Love-Pipeline v1.0", page_icon="🚀", layout="centered")

# --- Terminal-style CSS + Proposal CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Fira Code', 'Courier New', monospace;
}
.stApp {
    background-color: #0a0a0a;
}
h1, h2, h3, h4, p, li, span, label, div {
    color: #00ff41 !important;
}
.stButton > button {
    background-color: #1a1a2e;
    color: #00ff41;
    border: 1px solid #00ff41;
    font-family: 'Fira Code', monospace;
    font-size: 1.1rem;
    padding: 0.6rem 1.5rem;
    transition: all 0.3s;
}
.stButton > button:hover {
    background-color: #00ff41;
    color: #0a0a0a;
    border: 1px solid #00ff41;
}
.block-container { max-width: 750px; }

/* Terminal header bar */
.terminal-bar {
    background: #1a1a2e;
    border: 1px solid #00ff41;
    border-radius: 8px 8px 0 0;
    padding: 8px 16px;
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 0;
}
.terminal-dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
.dot-red { background: #ff5f56; }
.dot-yellow { background: #ffbd2e; }
.dot-green { background: #27c93f; }

.terminal-body {
    background: #0e1117;
    border: 1px solid #00ff41;
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 20px;
    margin-bottom: 20px;
}

/* Commit card */
.commit-card {
    background: #111;
    border-left: 3px solid #00ff41;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 0 6px 6px 0;
}
.commit-hash { color: #888 !important; font-size: 0.8rem; }
.commit-msg { color: #00ff41 !important; font-size: 1rem; font-weight: bold; }
.commit-date { color: #aaa !important; font-size: 0.85rem; }

/* Password input */
input[type="password"] {
    background-color: #111 !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    font-family: 'Fira Code', monospace !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: #111 !important;
    color: #00ff41 !important;
}

/* Blinking cursor effect */
@keyframes blink { 50% { opacity: 0; } }
.cursor { animation: blink 1s step-end infinite; color: #00ff41; }

/* Slideshow */
.slideshow-container {
    position: relative;
    width: 100%;
    overflow: hidden;
    border: 1px solid #00ff41;
    border-radius: 8px;
    background: #111;
}
.slideshow-container img {
    width: 100%;
    display: block;
    border-radius: 8px;
}

/* Proposal section */
.proposal-box {
    text-align: center;
    padding: 40px 20px;
    border: 2px solid #ff69b4;
    border-radius: 15px;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0a1a 100%);
    margin: 30px 0;
    position: relative;
    overflow: hidden;
}
.proposal-box h1 {
    color: #ff69b4 !important;
    font-size: 2rem;
    margin-bottom: 20px;
}
.proposal-box p {
    color: #ccc !important;
    font-size: 1.1rem;
}

/* YES button */
.yes-btn {
    background: #ff69b4 !important;
    color: #fff !important;
    border: none !important;
    font-size: 1.5rem !important;
    padding: 15px 60px !important;
    border-radius: 10px !important;
    cursor: pointer;
    font-family: 'Fira Code', monospace !important;
    font-weight: bold !important;
}
.yes-btn:hover {
    background: #ff1493 !important;
    color: #fff !important;
    transform: scale(1.1);
}
</style>
""", unsafe_allow_html=True)

# --- Data: Your Timeline ---
PHOTOS_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "photos")
# Docker fallback: non-root user path in container
if not os.path.isdir(PHOTOS_BASE):
    PHOTOS_BASE = "/home/eberrik/app/photos"

timeline = [
    {"date": "2nd April, 2025",  "tag": "our 1st meet",                          "hash": "a1b2c3d", "log": "Connection established... Handshake successful."},
    {"date": "4th April, 2025",  "tag": "Random meet",                            "hash": "e4f5g6h", "log": "Unexpected ping received... Connection accepted."},
    {"date": "7th April, 2025",  "tag": "Random meet",                            "hash": "i7j8k9l", "log": "Recurring sync detected... Pattern recognized."},
    {"date": "8th April, 2025",  "tag": "our 1st Shopping",                       "hash": "m0n1o2p", "log": "Deploying shopping_cart.exe... Budget overflow handled."},
    {"date": "11th April, 2025", "tag": "Random meet",                            "hash": "q3r4s5t", "log": "Heartbeat check... All systems nominal."},
    {"date": "12th April, 2025", "tag": "Kalighat",                               "hash": "u6v7w8x", "log": "Location service updated... Spiritual module loaded."},
    {"date": "1st May, 2025",    "tag": "Our 1st Month Anniversery",              "hash": "y9z0a1b", "log": "🎉 MILESTONE: 30 days uptime achieved! Zero downtime."},
    {"date": "4th May, 2025",    "tag": "She came to my home 1st time",           "hash": "c2d3e4f", "log": "Guest access granted to home_server... Welcome packet sent."},
    {"date": "6th May, 2025",    "tag": "Random meet",                            "hash": "g5h6i7j", "log": "Routine sync... Connection strength: STRONG."},
    {"date": "18th May, 2025",   "tag": "Her Parents came to my Place 1st time",  "hash": "k8l9m0n", "log": "Admin users connected to network... Firewall set to FRIENDLY."},
    {"date": "28th May, 2025",   "tag": "i went to her place 1st time",           "hash": "o1p2q3r", "log": "Remote deployment initiated... New environment explored."},
    {"date": "8th June, 2025",   "tag": "my parents went to her place 1st time",  "hash": "s4t5u6v", "log": "Cross-network handshake... Both clusters now linked."},
    {"date": "14th June, 2025",  "tag": "1st Movie date",                         "hash": "w7x8y9z", "log": "Streaming service activated... Popcorn module loaded."},
    {"date": "24th June, 2025",  "tag": "Belurmath",                              "hash": "a0b1c2d", "log": "Navigating to sacred node... Peace protocol engaged."},
    {"date": "25th June, 2025",  "tag": "Ecopark",                                "hash": "e3f4g5h", "log": "Outdoor module deployed... Nature API connected."},
    {"date": "26th Sept, 2025",  "tag": "1st Durga Puja Pandal Hopping",          "hash": "i6j7k8l", "log": "Festival mode ON... Pandal discovery service running."},
    {"date": "28th Sept, 2025",  "tag": "2nd day of Durga Puja",                  "hash": "m9n0o1p", "log": "Festival pipeline: Stage 2 executing... Joy overflow."},
    {"date": "2nd Oct, 2025",    "tag": "at her place Durga Puja",                "hash": "q2r3s4t", "log": "Merged into family cluster... Puja build successful."},
]

SECRET_PASSWORD = "31032025"  # Anniversary date: 31st March 2025

# --- Helper: typewriter effect ---
def typewriter(text, speed=0.03):
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(f"`{displayed}`<span class='cursor'>▌</span>", unsafe_allow_html=True)
        time.sleep(speed)
    placeholder.markdown(f"`{displayed}`", unsafe_allow_html=True)

# --- Helper: get photos for a date folder ---
def get_photos(date_tag_folder):
    folder = os.path.join(PHOTOS_BASE, date_tag_folder)
    if not os.path.isdir(folder):
        return []
    exts = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    return [os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.lower().endswith(exts)]

# --- Helper: collect ALL random meet photos ---
def get_all_random_meet_photos():
    all_photos = []
    for event in timeline:
        if event["tag"] == "Random meet":
            folder_name = f"{event['date']} ({event['tag']})"
            photos = get_photos(folder_name)
            for p in photos:
                all_photos.append({"path": p, "date": event["date"]})
    return all_photos

# --- Helper: image to base64 for HTML slideshow ---
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- Terminal Header ---
st.markdown("""
<div class="terminal-bar">
    <span class="terminal-dot dot-red"></span>
    <span class="terminal-dot dot-yellow"></span>
    <span class="terminal-dot dot-green"></span>
    <span style="color:#888; margin-left:12px; font-size:0.85rem;">eberrik@love-server:~/anniversary$</span>
</div>
<div class="terminal-body">
    <p style="margin:0;">EBERRIK-OS v1.0 — Anniversary Deployment System</p>
    <p style="margin:0; color:#888 !important;">Secure connection required. Enter access key to proceed.</p>
</div>
""", unsafe_allow_html=True)

# --- Password Gate ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "pipeline_run" not in st.session_state:
    st.session_state.pipeline_run = False
if "said_yes" not in st.session_state:
    st.session_state.said_yes = False

if not st.session_state.authenticated:
    st.markdown("#### 🔐 Authentication Required")
    pwd = st.text_input("Enter the secret key (hint: our anniversary date, DDMMYYYY):", type="password")
    if st.button("🔓 AUTHENTICATE"):
        if pwd == SECRET_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ ACCESS DENIED — Wrong key. Try again.")
    st.stop()

# --- Authenticated: Show Pipeline ---
st.markdown("#### 📟 EBERRIK-OS: Anniversary Deployment")
typewriter("Authentication successful. Welcome, love. 💚", speed=0.04)
st.markdown("---")

if st.button("🚀 RUN ANNIVERSARY PIPELINE"):
    st.session_state.pipeline_run = True

    # Stage 1: System Check
    with st.status("⚙️ Stage 1: System Integrity Check...", expanded=True) as s1:
        st.write("`Checking heart_rate_monitor... OK`")
        time.sleep(0.8)
        st.write("`Checking love_module... LOADED`")
        time.sleep(0.8)
        st.write("`Checking memory_bank... 18 commits found`")
        time.sleep(0.5)
        s1.update(label="✅ Stage 1: System Integrity Check — PASSED", state="complete")

    # Stage 2: Loading Timeline
    with st.status("📦 Stage 2: Loading Commit History...", expanded=True) as s2:
        st.write(f"`Fetching {len(timeline)} commits from relationship.git...`")
        time.sleep(1)
        st.write("`Branch: main | Status: STABLE | Uptime: counting...`")
        time.sleep(0.8)
        s2.update(label="✅ Stage 2: Commit History Loaded — PASSED", state="complete")

    # Stage 3: Deploying
    with st.status("🚀 Stage 3: Deploying Anniversary Package...", expanded=True) as s3:
        st.write("`Building memories.tar.gz...`")
        time.sleep(1)
        st.write("`Deploying to heart_server...`")
        time.sleep(1)
        st.write("`Deploy successful. All services GREEN.`")
        time.sleep(0.5)
        s3.update(label="✅ Stage 3: Deployment — SUCCESS", state="complete")

    st.balloons()

if st.session_state.pipeline_run:
    st.success("🟢 PIPELINE GREEN — All stages passed. Accessing Anniversary Archive...")
    st.markdown("---")

    # =============================================
    # RANDOM MEETS SLIDESHOW (only if photos exist)
    # =============================================
    random_photos = get_all_random_meet_photos()
    if random_photos:
        st.markdown("### 📸 Random Encounters — Slideshow")
        st.markdown("`cat /var/log/random_meets/*.jpg | slideshow --autoplay`")

        slides_html = ""
        for idx, photo in enumerate(random_photos):
            b64 = img_to_base64(photo["path"])
            ext = os.path.splitext(photo["path"])[1].lower()
            mime = "image/jpeg" if ext in (".jpg", ".jpeg") else f"image/{ext.replace('.', '')}"
            display = "block" if idx == 0 else "none"
            slides_html += f'''
            <div class="slide" style="display:{display};">
                <img src="data:{mime};base64,{b64}" style="width:100%; border-radius:8px;">
                <p style="text-align:center; color:#888 !important; margin-top:8px; font-size:0.85rem;">
                    📅 {photo["date"]} — Random meet #{idx+1}
                </p>
            </div>'''

        st.markdown(f"""
        <div class="slideshow-container" id="randomSlideshow">
            {slides_html}
        </div>
        <div style="text-align:center; margin-top:10px;">
            <button onclick="prevSlide()" style="background:#1a1a2e; color:#00ff41; border:1px solid #00ff41; padding:8px 20px; border-radius:5px; cursor:pointer; font-family:'Fira Code',monospace; margin:0 5px;">◀ Prev</button>
            <button onclick="nextSlide()" style="background:#1a1a2e; color:#00ff41; border:1px solid #00ff41; padding:8px 20px; border-radius:5px; cursor:pointer; font-family:'Fira Code',monospace; margin:0 5px;">Next ▶</button>
        </div>
        <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('#randomSlideshow .slide');
        let autoTimer = setInterval(nextSlide, 3000);

        function showSlide(n) {{
            slides.forEach(s => s.style.display = 'none');
            currentSlide = (n + slides.length) % slides.length;
            slides[currentSlide].style.display = 'block';
        }}
        function nextSlide() {{ showSlide(currentSlide + 1); }}
        function prevSlide() {{ showSlide(currentSlide - 1); clearInterval(autoTimer); autoTimer = setInterval(nextSlide, 3000); }}
        </script>
        """, unsafe_allow_html=True)
        st.markdown("---")

    # =============================================
    # COMMIT HISTORY (Timeline)
    # =============================================
    st.markdown("### 📖 Commit History — Our Story So Far")
    st.markdown("`git log --oneline --all --graph`")
    st.markdown("")

    for i, event in enumerate(timeline):
        folder_name = f"{event['date']} ({event['tag']})"
        photos = get_photos(folder_name)
        is_random = event["tag"] == "Random meet"

        with st.expander(f"📌 commit {event['hash']} — {event['date']}: {event['tag']}"):
            st.markdown(f"""
<div class="commit-card">
    <div class="commit-hash">commit {event['hash']}</div>
    <div class="commit-date">Date: {event['date']}</div>
    <div class="commit-msg">{event['tag']}</div>
</div>
            """, unsafe_allow_html=True)
            st.code(f"$ cat deploy.log\n{event['log']}", language="bash")

            if photos:
                if is_random:
                    # Slideshow for individual Random meet
                    st.caption("🎞️ Slideshow mode — Random encounter memories")
                    slide_key = f"slide_{i}"
                    if slide_key not in st.session_state:
                        st.session_state[slide_key] = 0
                    idx = st.session_state[slide_key] % len(photos)
                    st.image(photos[idx], use_container_width=True)
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        if st.button("◀ Prev", key=f"prev_{i}"):
                            st.session_state[slide_key] -= 1
                            st.rerun()
                    with col3:
                        if st.button("Next ▶", key=f"next_{i}"):
                            st.session_state[slide_key] += 1
                            st.rerun()
                    with col2:
                        st.caption(f"Photo {idx+1} of {len(photos)}")
                else:
                    cols = st.columns(min(len(photos), 3))
                    for idx, photo in enumerate(photos):
                        with cols[idx % 3]:
                            st.image(photo, use_container_width=True)
            else:
                st.caption("📂 No photos deployed yet — add them to the photos folder!")

    # =============================================
    # FINAL MESSAGE
    # =============================================
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:30px; border:1px solid #00ff41; border-radius:10px; background:#0e1117;">
        <h2 style="color:#00ff41 !important;">💚 DEPLOYMENT COMPLETE 💚</h2>
        <p style="color:#ccc !important; font-size:1.1rem;">
            Every commit, every merge, every deploy —<br>
            it all led to <strong style="color:#00ff41 !important;">us</strong>.<br><br>
            Here's to infinite more commits on our <code>main</code> branch. 🚀
        </p>
        <p style="color:#888 !important; font-size:0.85rem; margin-top:20px;">
            — with love, from eberrik@love-server
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =============================================
    # 💍 PROPOSAL SECTION
    # =============================================
    st.markdown("---")
    st.markdown("### 🔓 Unlocking Final Stage: proposal.exe")
    st.code("$ sudo ./proposal.exe --mode=forever --no-rollback", language="bash")
    time.sleep(0.5)

    st.markdown("""
    <div class="proposal-box">
        <p style="color:#ff69b4 !important; font-size:0.9rem;">CRITICAL DEPLOYMENT — REQUIRES MANUAL APPROVAL</p>
        <h1 style="color:#ff69b4 !important;">💍 Will You Marry Me? 💍</h1>
        <p style="color:#aaa !important;">This deployment is <strong style="color:#ff69b4 !important;">irreversible</strong>. No rollback available.</p>
    </div>
    """, unsafe_allow_html=True)

    import streamlit.components.v1 as components

    proposal_html = """
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Fira Code', monospace; }
        body { background: #0a0a0a; }
        #proposal-buttons {
            text-align: center; padding: 20px;
            position: relative; min-height: 200px;
        }
        #yesBtn {
            background: #ff69b4; color: white; border: none;
            font-size: 1.5rem; padding: 15px 60px; border-radius: 10px;
            cursor: pointer; font-family: 'Fira Code', monospace;
            font-weight: bold; margin: 10px; display: inline-block;
        }
        #yesBtn:hover { background: #ff1493; transform: scale(1.1); }
        #noBtn {
            background: #333; color: #888; border: 1px solid #555;
            font-size: 1.2rem; padding: 12px 40px; border-radius: 10px;
            cursor: pointer; font-family: 'Fira Code', monospace;
            margin: 10px; display: inline-block; position: relative;
            transition: all 0.3s;
        }
        #yes-celebration {
            display: none; text-align: center; padding: 30px;
        }
        #yes-celebration h1 { color: #ff69b4; font-size: 2.2rem; }
        #yes-celebration p { color: #00ff41; font-size: 1.1rem; margin: 10px 0; }
        #yes-celebration .emojis { font-size: 3rem; }
    </style>
    </head>
    <body>
        <div id="proposal-buttons">
            <button id="yesBtn" onclick="sayYes()">✅ YES</button>
            <button id="noBtn">❌ NO</button>
        </div>
        <div id="yes-celebration">
            <h1>💖💍 SHE SAID YES! 💍💖</h1>
            <p>$ git merge love --no-ff --message="forever together"</p>
            <p>Merge successful. No conflicts found. 💚</p>
            <p class="emojis">🎉🎊💐💖🥂</p>
        </div>
        <script>
        function sayYes() {
            document.getElementById('proposal-buttons').style.display = 'none';
            document.getElementById('yes-celebration').style.display = 'block';
        }

        var noBtn = document.getElementById('noBtn');
        var container = document.getElementById('proposal-buttons');

        function moveNoBtn() {
            var maxX = container.offsetWidth - noBtn.offsetWidth - 20;
            var maxY = 120;
            var randX = Math.floor(Math.random() * Math.max(maxX, 100));
            var randY = Math.floor(Math.random() * maxY);
            noBtn.style.position = 'absolute';
            noBtn.style.left = randX + 'px';
            noBtn.style.top = randY + 'px';
        }

        // Desktop: mouse hover makes it run away
        noBtn.addEventListener('mouseover', moveNoBtn);

        // Desktop: clicking also makes it run
        noBtn.addEventListener('click', function(e) {
            e.preventDefault();
            moveNoBtn();
        });

        // Mobile: touch converts NO to YES
        noBtn.addEventListener('touchstart', function(e) {
            e.preventDefault();
            noBtn.innerText = '✅ YES';
            noBtn.style.background = '#ff69b4';
            noBtn.style.color = 'white';
            noBtn.style.border = 'none';
            noBtn.style.fontSize = '1.5rem';
            noBtn.style.position = 'relative';
            noBtn.removeEventListener('mouseover', moveNoBtn);
            noBtn.onclick = sayYes;
        });
        </script>
    </body>
    </html>
    """
    components.html(proposal_html, height=350)

    # =============================================
    # 📂 BONUS TABS: Changelog + Certificate + Registry
    # =============================================
    st.markdown("---")
    st.markdown("### 📂 Bonus Artifacts")
    st.code("$ ls /var/artifacts/", language="bash")

    tab1, tab2, tab3 = st.tabs(["📜 Changelog", "🏆 Certificate", "🗄️ Registry"])

    # --- TAB 1: Love Changelog ---
    with tab1:
        st.markdown("#### 📜 The Love Changelog")
        st.markdown("`cat CHANGELOG.md`")

        changelog = [
            {"ver": "v0.0.1-alpha", "date": "31st March, 2025", "title": "Genesis — The Beginning",
             "desc": "Initial commit. Two souls connected. Repository initialized.",
             "features": ["First spark detected", "Butterflies module loaded", "Future.exe initialized"]},
            {"ver": "v0.1.0-beta", "date": "2nd April, 2025", "title": "First Handshake",
             "desc": "Connection established. Low latency, high chemistry.",
             "features": ["Eye contact protocol established", "Smile.js compiled successfully", "First laugh — zero bugs"]},
            {"ver": "v0.2.0", "date": "8th April, 2025", "title": "Shopping Cart Deployment",
             "desc": "First joint resource allocation exercise. Budget overflow handled gracefully.",
             "features": ["Shared wallet module tested", "Patience.exe stress-tested", "Happiness index: HIGH"]},
            {"ver": "v0.5.0", "date": "1st May, 2025", "title": "30-Day Uptime Milestone",
             "desc": "System achieved 30 consecutive days without incident. Stability confirmed.",
             "features": ["Zero downtime recorded", "Love module upgraded to v2", "Monthly anniversary cron job set"]},
            {"ver": "v0.8.0", "date": "8th June, 2025", "title": "Cross-Network Merge",
             "desc": "Both family clusters successfully linked. Full integration achieved.",
             "features": ["Parent nodes connected", "Trust handshake complete", "Family firewall: OPEN"]},
            {"ver": "v1.0.0-LTS", "date": "31st March, 2026", "title": "Anniversary v1.0 — Long Term Support",
             "desc": "365 days of 99.99% uptime. The most stable release in production.",
             "features": ["Permanent residency in my heart", "Unlimited support plan activated", "No end-of-life date"]},
        ]

        for entry in changelog:
            with st.expander(f"🛠️ {entry['ver']} — {entry['title']}"):
                st.caption(f"📅 {entry['date']}")
                st.write(entry["desc"])
                st.markdown("**Changes:**")
                for feat in entry["features"]:
                    st.markdown(f"- ✅ {feat}")

    # --- TAB 2: Stability Certificate ---
    with tab2:
        st.markdown("#### 🏆 Certificate of Stability")
        st.code("$ openssl x509 -in love_cert.pem -text", language="bash")

        if HAS_PIL:
            if st.button("🔏 Generate & Download Certificate"):
                with st.spinner("Cryptographically signing the love artifact..."):
                    width, height = 1123, 794
                    bg = (10, 10, 10)
                    green = (0, 255, 65)
                    pink = (255, 105, 180)
                    white = (255, 255, 255)
                    grey = (136, 136, 136)

                    img = Image.new("RGB", (width, height), bg)
                    draw = ImageDraw.Draw(img)

                    draw.rectangle([(30, 30), (width-30, height-30)], outline=green, width=3)
                    draw.rectangle([(40, 40), (width-40, height-40)], outline=pink, width=1)

                    try:
                        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 42)
                        font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 28)
                        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22)
                    except OSError:
                        font_big = ImageFont.load_default()
                        font_med = ImageFont.load_default()
                        font_sm = ImageFont.load_default()

                    draw.text((width//2, 90), "CERTIFICATE OF STABILITY", fill=green, font=font_big, anchor="mm")
                    draw.text((width//2, 140), "Relationship v1.0 — Long Term Support", fill=pink, font=font_med, anchor="mm")
                    draw.line([(200, 175), (width-200, 175)], fill=green, width=2)

                    lines = [
                        (240, "This certifies that the system connection", white, font_sm),
                        (280, "established between [Her Name] & Eberrik", green, font_med),
                        (320, "has achieved 100% CORE STABILITY.", white, font_sm),
                        (400, "365 DAYS WITHOUT INCIDENT", pink, font_big),
                        (470, "This LTS release guarantees perpetual maintenance,", grey, font_sm),
                        (510, "zero unplanned downtime, and unlimited memory.", grey, font_sm),
                        (550, "Deployment authorized for: FOREVER", green, font_med),
                    ]
                    for y, text, color, font in lines:
                        draw.text((width//2, y), text, fill=color, font=font, anchor="mm")

                    today = datetime.date.today().strftime("%B %d, %Y")
                    draw.text((150, height-100), "Signed: eberrik", fill=green, font=font_sm, anchor="lm")
                    draw.text((150, height-70), "Lead DevOps Engineer", fill=grey, font=font_sm, anchor="lm")
                    draw.text((width-150, height-100), f"Date: {today}", fill=green, font=font_sm, anchor="rm")
                    draw.text((width-150, height-70), "Howrah, WB", fill=grey, font=font_sm, anchor="rm")

                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    st.image(buf.getvalue(), caption="Certificate of Stability — v1.0 LTS", use_container_width=True)
                    st.download_button(
                        label="📥 Download Certificate",
                        data=buf.getvalue(),
                        file_name="Stability_Certificate_v1.0.png",
                        mime="image/png"
                    )
        else:
            st.warning("Pillow not installed. Certificate generation unavailable.")

    # --- TAB 3: Registry Browser ---
    with tab3:
        st.markdown("#### 🗄️ Love-Artifact Registry")
        st.code("$ curl -s registry.eberrik.local:5000/v2/_catalog | jq", language="bash")

        try:
            import requests
            REGISTRY_URL = os.environ.get("REGISTRY_URL", "http://registry.eberrik.local:5000/v2")
            REG_USER = os.environ.get("REGISTRY_USER", "eberrik")
            REG_PASS = os.environ.get("REGISTRY_PASS", "")

            auth = (REG_USER, REG_PASS) if REG_PASS else None

            try:
                resp = requests.get(f"{REGISTRY_URL}/_catalog", auth=auth, timeout=5)
                repos = resp.json().get("repositories", [])

                if repos:
                    for repo in repos:
                        tags_resp = requests.get(f"{REGISTRY_URL}/{repo}/tags/list", auth=auth, timeout=5)
                        tags = tags_resp.json().get("tags", [])
                        with st.expander(f"📦 {repo} — {len(tags)} tag(s)"):
                            for tag in sorted(tags, reverse=True):
                                st.markdown(f"""
<div class="commit-card">
    <div class="commit-hash">{repo}:{tag}</div>
    <div class="commit-msg">docker pull registry.eberrik.local:5000/{repo}:{tag}</div>
</div>
                                """, unsafe_allow_html=True)
                else:
                    st.info("Registry is empty. Push your first image!")
            except requests.exceptions.ConnectionError:
                st.warning("Cannot connect to registry.eberrik.local:5000 — is it running?")
        except ImportError:
            st.warning("`requests` not installed. Registry browser unavailable.")
