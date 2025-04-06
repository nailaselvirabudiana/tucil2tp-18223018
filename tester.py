import requests
import pyotp
import base64
import time
import json

users = {
    "sister": "ii2210_sister_astro123",
    "naila": "ii2210_cosmic456"
}

server_url = "http://57.155.90.211:17787/motd"

motd_list = [
    "The universe speaks in many ways, through stars, planets, and cosmic whispers. Listen closely to hear its guidance.",
    "Today's cosmic alignment suggests a time of reflection. Look within to find the answers you seek among the stars.",
    "The gravitational pull of your dreams is stronger than you think. Let it guide your journey through the cosmos.",
    "Just as stars form from cosmic dust, great achievements arise from small beginnings. Start your journey today.",
    "Like the phases of the moon, life has its cycles. Embrace the darkness, for it makes the light more beautiful.",
    "Your potential is as vast as the universe itself. Expand beyond your current boundaries into new galaxies of possibility.",
    "Time is relative. What matters is not how much time you have, but how you use the time given to you in this cosmic dance.",
    "We are all made of stardust, connected through the fabric of spacetime. Remember your cosmic origins.",
    "As the planets orbit the sun, your life orbits your purpose. Find your center and maintain your trajectory.",
    "The universe rewards curiosity. Explore the unknown territories of your mind and discover new constellations of thought.",
    "Black holes teach us that even the most powerful forces can't destroy information. Your impact on others is eternal.",
    "Today the cosmos reminds us that sometimes the most beautiful phenomena occur after periods of chaos and uncertainty.",
    "Like distant galaxies expanding, your consciousness is always growing. Nurture its development with new experiences.",
    "The light of distant stars takes years to reach us. Your actions today may not show results immediately, but patience will reveal their brilliance.",
    "Quantum entanglement reminds us that once connected, two particles remain influenced by each other regardless of distance. Choose your connections wisely."
]


for userid, shared_secret in users.items():
    for motd in motd_list:
        s = base64.b32encode(shared_secret.encode("utf-8")).decode("utf-8")
        totp = pyotp.TOTP(s=s, digest="SHA256", digits=8)
        token = totp.now()
        
        auth_str = f"{userid}:{token}"
        auth_encoded = base64.b64encode(auth_str.encode("ascii")).decode("ascii")

        headers = {
            "Authorization": f"Basic {auth_encoded}"
        }

        response = requests.post(url=server_url, headers=headers, json={"motd": motd})
        print(response.content.decode("utf-8"))
        time.sleep(1)
