"use client"
import { generateKeyPair } from "@/app/lib/devicekey"

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL

export default function LoginPage() {
  async function handleSubmit(e: any) {
    e.preventDefault()

    const formData = new FormData(e.target)
    const keyPair = await generateKeyPair()
    const publicKey = await window.crypto.subtle.exportKey("jwk", keyPair.publicKey)
    
    // runs once per browser profile
    let deviceId = localStorage.getItem("device_id");

    if (!deviceId) {
      deviceId = crypto.randomUUID();
      localStorage.setItem("device_id", deviceId);
    }

    const res = await fetch(`${apiBaseUrl}/user/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: formData.get("username"),
        password: formData.get("password"),
        public_key_pem: publicKey,
        device_id: deviceId,
      }),
    })

    const data = await res.json()
    console.log(data)
    window.alert("Login successful!")
  }

  return (
    <form onSubmit={handleSubmit}>
      <h3>Login</h3>

      <input name="username" placeholder="username" />
      <input name="password" type="password" placeholder="password" />

      <button type="submit">Login</button>
    </form>
  )
}
