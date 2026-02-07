<script setup lang='ts'>
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';

const props = defineProps<{
    title: string;
    visible: boolean;
    handleClose: () => void;
}>();

</script>

<template>
    <Dialog
        :visible='visible'
        modal
        :header='props.title'
        @update:visible='props.handleClose'
    >
        <div class='flex flex-col items-center'>
            <span class='text-surface-500 dark:text-surface-400 block mb-2'>Update your username</span>

            <div class='flex items-center gap-4 mb-4'>
                <label for='username' class='font-semibold w-24'>Username</label>
                <InputText id='username' class='flex-auto' autocomplete='off' />
            </div>
        </div>

        <div class='flex justify-end gap-2'>
            <Button
                label='Cancel'
                severity='secondary'
                @click='props.handleClose'
            />

            <Button
                label='Save'
                @click='props.handleClose'
            />
        </div>
    </Dialog>
</template>

<!-- <style>
@import url('./ChangePopup.css');
</style> -->