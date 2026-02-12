import { FetchWithFormData } from '../api';

export const VerifyImages = (files: File[]): [boolean, string] => {
    files.forEach(file => {
        if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
            return [false, 'Only JPG, PNG, and WEBP images are allowed.'];
        }

        if (file.size > 15 * 1024 * 1024) {
            return [false, 'Each image must be less than 15MB.'];
        }
    })

    return [true, ''];
}

export const CreatePost = async (
    title: string,
    body: string,
    status: 'Private' | 'Public',
    images: File[],
    toastAdd: (title: string, message: string, severity?: 'success' | 'info' | 'warn' | 'error') => void,
    routerPush: (path: string) => void,
    setLoading: (loading: boolean) => void
) => {
    setLoading(true);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('body', body);
    formData.append('status', status.toUpperCase());

    images.forEach((image, _) => {
        formData.append('images', image);
    });

    FetchWithFormData('post/create_post/', {
        method: 'POST',
        body: formData
    })
    .then(async response => {
        const status = response.status;
        const data = await response.json();

        if (status !== 201) {
            toastAdd('Error while creating post', data.error || 'Failed to create post.', 'error');
            return;
        }

        routerPush(`/post?post_id=${data.post.id}`);
    }).finally(() => {
        setLoading(false);
    });
}