import { getToken } from "./tokenFunctions";
const SERVER_URL = "http://localhost:5000";

export const createUserApi = async ({ email, password, roleId }) => {
  /**
   * Creates a new user
   * @param {Object} userData - The user's data
   * @param {string} userData.email - The user's email
   * @param {string} userData.password - The user's password
   * @param {int} userData.roleId - The user's role id
   * @returns {void}
   **/

  const token = getToken();
  try {
    const res = await fetch(`${SERVER_URL}/api/users`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password, roleId }),
    });

    const response = await res.json();

    if (!res.ok) {
      console.log(response.error);
      throw new Error(response.description);
    }
  } catch (error) {
    throw new Error(`Create User Failed: ${error.message}`);
  }
};

// TODO: Probably remove limit
export const getUsersApi = async ({
  searchField,
  sortBy,
  sortOrder,
  page,
  limit,
}) => {
  /**
   * Gets all users
   * @param {Object} args - The fetch filter
   * @param {string} args.searchField - The search value
   * @param {string} args.sortBy - The sort field
   * @param {string} args.sortOrder - The sort order wanted
   * @param {int} args.page - The page number
   * @param {int} args.limit - The limit
   * @returns {Array} - The users
   **/

  const token = getToken();
  try {
    const res = await fetch(
      `${SERVER_URL}/api/users?search=${searchField}&sortBy=${sortBy}&sortOrder=${sortOrder}&page=${page}&limit=${limit}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );
    const response = await res.json();

    if (!res.ok) {
      console.error(response.error);
      throw new Error(response.description);
    } else {
      return response.users;
    }
  } catch (error) {
    throw new Error(`Fetch Users Failed: ${error.message}`);
  }
};

export const deleteUserApi = async (userId) => {
  /**
   * Deletes a user
   * @param {int} userId - The user's id
   * @returns {void}
   **/

  const token = getToken();
  try {
    const res = await fetch(`${SERVER_URL}/api/users/${userId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    const response = await res.json();

    if (!res.ok) {
      console.error(response.error);
      throw new Error(response.description);
    } else {
    }
  } catch (error) {
    throw new Error(`Delete Failed: ${error.message}`);
  }
};

export const updateUserApi = async ({ userId, email, roleId }) => {
  /**
   * Updates a user
   * @param {Object} userData - The user's new data
   * @param {int} userData.userId - The user's id
   * @param {string} userData.email - The user's email
   * @param {int} userData.roleId - The user's role id
   * @returns {void}
   **/

  const token = getToken();
  try {
    const res = await fetch(`${SERVER_URL}/api/users/${userId}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, roleId }),
    });

    const response = await res.json();

    if (!res.ok) {
      console.error(response.error);
      throw new Error(response.description);
    } else {
      if (response.description) {
        return "No Changes Made";
      } else {
        return "";
      }
    }
  } catch (error) {
    throw new Error(`Edit User Failed: ${error.message}`);
  }
};

export const getRolesApi = async () => {
  /**
   * Retrieves the roles
   * @returns {Array} - The roles, an array of dicts with id and name
   **/

  const token = getToken();
  try {
    const res = await fetch(`${SERVER_URL}/api/roles`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    const response = await res.json();

    if (!res.ok) {
      console.error(response.error);
      throw new Error(response.description);
    }

    return response.roles;
  } catch (error) {
    throw new Error(`Failed To Retrieve Roles: ${error.message}`);
  }
};
