import type { ToastMessageOptions } from 'primevue';
import { Fetch } from '../api';

export const EditUsername = (
    username: string,
    toastAdd: (message: ToastMessageOptions) => void
) => {
    const [usernameValid, usernameInvalidMessage] = verifyUsername(username); 
    if (!usernameValid) {
        toastAdd({
            severity: 'error',
            summary: 'Input invalid',
            detail: usernameInvalidMessage,
            life: 3000
        });

        return;
    }

    Fetch('user/change_username/', {
        method: 'PUT',
        body: JSON.stringify({
            new_username: username
        })
    })
    .then(async res => {
        const status = res.status;
        const data = await res.json();

        if (status !== 200) {
            toastAdd({
                severity: 'error',
                summary: 'Server error',
                detail: data.message,
                life: 3000
            });

            return;
        }

        toastAdd({
            severity: 'success',
            summary: 'Success',
            detail: 'Successfully updated username',
            life: 3000
        });
    });
}

const verifyUsername = (username: string): [boolean, string | null] => {
    const pattern = /^[a-zA-Z0-9_]*$/;

    if (!pattern.test(username)) {
        return [false, 'Username must have only alphanumeric characters and underscores'];
    }

    if (username.length < 7 || username.length > 15) {
        return [false, 'Username must be between (not including) 7 and 15 characters long.'];
    }

    return [true, null];
}

export const EditName = (
    name: string,
    toastAdd: (message: ToastMessageOptions) => void
) => {
    const [nameValid, nameInvalidMessage] = verifyName(name); 
    if (!nameValid) {
        toastAdd({
            severity: 'error',
            summary: 'Input invalid',
            detail: nameInvalidMessage,
            life: 3000
        });

        return;
    }

    Fetch('user/set_name/', {
        method: 'PUT',
        body: JSON.stringify({
            new_name: name
        })
    })
    .then(async res => {
        const status = res.status;
        const data = await res.json();

        if (status !== 200) {
            toastAdd({
                severity: 'error',
                summary: 'Server error',
                detail: data.message,
                life: 3000
            });

            return;
        }

        toastAdd({
            severity: 'success',
            summary: 'Success',
            detail: 'Successfully updated username',
            life: 3000
        });
    });
}

const verifyName = (name: string): [boolean, string | null] => {
    if (!name) return [true, null];

    if (name.length < 3 || name.length > 30)
        return [false, 'Name must be between (not including) 3 and 30 characters long'];

    const pattern = /^[\p{L}][\p{L}\p{M}'\-.\s]*$/u;
    if (!pattern.test(name)) {
        return [false, 'Name must contain only normal characters'];
    }

    return [true, null];
}