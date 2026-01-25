import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check for saved session
        const savedUser = localStorage.getItem('triageUser');
        if (savedUser) {
            setUser(JSON.parse(savedUser));
        }
        setLoading(false);
    }, []);

    const login = (username, password, rememberMe) => {
        // In a real app, this would be an API call
        // For now, we simulate a login by checking against "registered" users in localStorage
        // or just allowing any login if we don't strictly enforce registration for this demo phase yet.
        // However, the requirement says "requires doctor or nurse sign up".

        // Let's implement a simple check against stored users
        const users = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
        const foundUser = users.find(u => u.username === username && u.password === password);

        if (foundUser) {
            const userData = { name: foundUser.name, role: foundUser.role, username: foundUser.username };
            setUser(userData);
            if (rememberMe) {
                localStorage.setItem('triageUser', JSON.stringify(userData));
            } else {
                sessionStorage.setItem('triageUser', JSON.stringify(userData)); // Optional: session storage
            }
            return { success: true };
        } else {
            return { success: false, message: 'Invalid username or password' };
        }
    };

    const signup = (name, role, username, password) => {
        const users = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
        if (users.find(u => u.username === username)) {
            return { success: false, message: 'Username already exists' };
        }

        const newUser = { name, role, username, password }; // Note: Storing plain password is NOT secure for real apps
        users.push(newUser);
        localStorage.setItem('registeredUsers', JSON.stringify(users));

        // Auto login after signup? Or require login?
        // Let's require login to be explicit or just auto-login.
        // Requirement says "sign up ... and then sign in".
        return { success: true };
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('triageUser');
        sessionStorage.removeItem('triageUser');
    };

    return (
        <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
