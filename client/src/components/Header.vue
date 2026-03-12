<script lang='ts' setup>
import { ref } from 'vue';

import { verifyUser } from '../api';

import Drawer from 'primevue/drawer';

const drawerVisible = ref<boolean>(false);
const pfpSource = ref<string>('/default-pfp.png');

const fetchPfp = async () => {
    verifyUser().then(res => {
        if (res.result.user.pfp) pfpSource.value = res.result.user.pfp;
    });
}

fetchPfp();

</script>

<template>
    <div id='header'>
        <img :src='pfpSource' @click='drawerVisible = true' style='width: 75px; height: 75px; '>
        <Drawer v-model:visible='drawerVisible'>
            Test drawer
        </Drawer>
    </div>
</template>