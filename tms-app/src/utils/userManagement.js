const SERVER_URL = "http://localhost:5000";

export const createUser = async ({ email, password, role }) => {
  try {
    const res = await fetch(`${SERVER_URL}/api/admin/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password, role }),
    });

    const response = await res.json();

    if (!res.ok) {
      throw new Error(response.error);
    } else {
      console.log("User Created");
    }
  } catch (error) {
    throw new Error(`Login failed ${response.error}`);
  }
};
