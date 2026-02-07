<script setup lang='ts'>
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';

const props = defineProps<{
    visible: boolean,
    title: string,
    closeWindow: () => void
}>();

</script>

<template>
    <Dialog
        :visible='visible'
        modal
        :header='props.title'
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
                @click='props.closeWindow'
            />

            <Button
                label='Save'
                @click='props.closeWindow'
            />
        </div>
    </Dialog>
</template>

<!-- <style>
@import url('./ChangePopup.css');
</style> -->