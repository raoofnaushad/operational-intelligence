import { IUser } from "@/types/User";
import { fetcher } from "./fetcher";

export async function getCurrentUser(cookies: string): Promise<IUser|null> {
    const res = await fetcher('/api/users/me', {}, {
        headers: { 
            Cookie: cookies 
        },
    });

    if (res.status === 401) {
        return null
    }

    return res.data
}

