import type { ToastMessageOptions } from 'primevue/toast';
import { FetchWithFileUpload } from '../api';

export const UploadPFP = (
    image: File, toastAdd:
    (message: ToastMessageOptions) => void,
    setLoading: (value: boolean) => void
) => {
    setLoading(true);
    const data = new FormData();
    data.append('image', image);

    FetchWithFileUpload('pfp/create_user_pfp/', {
        method: 'POST'
    }, image, 'image')
    .then(async res => {
        const status = res.status;
        const data = await res.json();

        if (status !== 201) {
            toastAdd({
                severity: 'error',
                summary: 'Error while uploading',
                detail: data.message,
                life: 3000
            });
            return;
        }

        toastAdd({
            severity: 'success',
            summary: 'Success',
            detail: 'Successfully uploaded new PFP'
        });
    }).finally(() => {
        setLoading(false);
    });
}