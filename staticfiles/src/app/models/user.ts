export interface UserLoginRequest {
    username: string;
    password: string;
}

// export interface LoginUserDetail {
//     refresh?: string;
//     access?: string;
//     user?: UserDetail;
//     detail?: string
// }

export interface LoginUserDetail {
    email: string;
    last_login: string;
    session_id: string;
    token: string;
    token_expiration: string;
    user_id: number;
    first_name: string;
    last_name: string;
}

// export interface UserDetail {
//     id: number;
//     username: string;
//     first_name: string;
//     last_name: string;
//     last_login: string;
//     is_superuser: boolean;
//     is_staff: boolean;
//     is_active: boolean;
//     date_joined: string;
//     user_permissions: any[];
//     groups: any[];
// }

export interface ContactUs {
    Full_name: string;
    Company: string;
    Business_email: string;
    Contact_number: string;
}

export interface RequestDemo {
    Full_name: string;
    Company: string;
    Business_email: string;
    Contact_number: string;
}

export interface HelpAndSupport {
    Full_name: string;
    Company: string;
    Business_email: string;
    Contact_number: string;
}