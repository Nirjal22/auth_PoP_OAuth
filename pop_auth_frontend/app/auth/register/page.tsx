"use client"

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL

export default function RegisterPage() {
  async function handleSubmit(e: any) {
    e.preventDefault()

    const formData = new FormData(e.target)

    const res = await fetch(`${apiBaseUrl}/user/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: formData.get("username"),
        email: formData.get("email"),
        first_name: formData.get("first_name"),
        last_name: formData.get("last_name"),
        password: formData.get("password"),
      }),
    })

    const data = await res.json()
    console.log(data)
    window.alert("Registration successful! Please log in.")
  }

  return (
    <form onSubmit={handleSubmit}>
      <h3>Register</h3>

      <input name="username" placeholder="username" />
      <input name="email" placeholder="email" />
      <input name="first_name" placeholder="first name" />
      <input name="last_name" placeholder="last name" />
      <input name="password" type="password" placeholder="password" />

      <button type="submit">Register</button>
    </form>
  )
}
