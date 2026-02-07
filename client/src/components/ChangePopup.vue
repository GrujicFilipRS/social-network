<script setup lang='ts'>
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

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