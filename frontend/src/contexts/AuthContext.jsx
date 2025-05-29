import { createContext, useContext, useEffect, useState } from "react";
import { API } from "../api";

const AuthContext = createContext()

export const useAuth = () => useContext(AuthContext)

export const AuthContextProvider = ({ children }) => {
	const [user, setUser] = useState(null)
	const [loading, setLoading] = useState(true)

	useEffect(() => {
		const whoami = async () => {
			try {
				await fetch(API.csrf, {
					method: 'GET',
					credentials: 'include'
				})

				const response = await fetch(API.whoami, {
					method: 'GET',
					credentials: 'include'
				})

				const data = await response.json()

				if (response.status === 200) {
					setUser({
						id: data.user['id'],
						username: data.user['username'],
						email: data.user['email'],
						first_name: data.user['first_name'],
						last_name: data.user['last_name'],
					})
				}
			}
			catch {
				console.log('Something went wrong')
			}
			finally {
				setTimeout(() => setLoading(false), 300)
			}
		}

		whoami()
	}, [loading])

	return (
		<AuthContext.Provider value={{ user, setUser, loading, setLoading }}>
			{children}
		</AuthContext.Provider>
	)
}