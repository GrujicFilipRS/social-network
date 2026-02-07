<script setup lang='ts'>
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

const props = defineProps<{
    visible: boolean,
    title: string
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
            />
            <Button
                label='Save'
            />
        </div>
    </Dialog>
</template>

<style>
@import url('./ChangePopup.css');
</style>