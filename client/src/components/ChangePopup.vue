<script setup lang='ts'>
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import { ref, watch } from 'vue';

const props = defineProps<{
    title: string;
    originalValue: string;
    visible: boolean;
    handleClose: () => void;
}>();

const inputValue = ref<string>(props.originalValue);

watch(
    () => props.originalValue,
    (newValue) => {
        inputValue.value = newValue;
    }
)

</script>

<template>
    <Dialog
        :visible='visible'
        modal
        :header='`Change your ${title}`'
        @update:visible='props.handleClose'
    >
        <div class='flex flex-col items-center'>
            <div class='flex items-center gap-4 mb-4'>
                <label for='username' class='font-semibold w-24'>
                    {{ title.charAt(0).toUpperCase() + title.slice(1) }}:
                </label>
                <InputText id='username' class='flex-auto' autocomplete='off' v-model='inputValue' />
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