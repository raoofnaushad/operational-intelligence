'use client'

import { IUser } from "@/types/User"
import { createContext, Dispatch, useState, useContext } from 'react'

export interface IUserContext {
    user: IUser|null,
    setUser: Dispatch<IUser|null>
}
const UserContext = createContext<IUserContext|undefined>(undefined)

interface IProps {
    children: React.ReactNode, 
    initialValue: IUser|null
}

export const UserContextProvider = ({ children, initialValue } : IProps) => {
    const [user, setUser] = useState<IUser|null>(initialValue)
    
    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    )   
}

export const useUserContext = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUserContext must be used within a UserContextProvider');
    }
    return context;
};