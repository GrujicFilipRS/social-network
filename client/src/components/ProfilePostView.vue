<script setup lang='ts'>
import type { PostData } from '../interfaces/PostData';

const { postData } = defineProps<{postData: PostData}>();

const shortenString = (
    input: string,
    maxLength: number,
    maxRows?: number
): string => {
    let result = input;

    if (maxRows) {
        const rows = result.split('\n');
        if (rows.length > maxRows) {
            result = rows.slice(0, maxRows).join('\n');
            return result + '...';
        }
    }

    if (result.length > maxLength) {
        return result.slice(0, maxLength) + '...';
    }

    return result;
};

</script>

<template>
    <div class='post mb-4'>
        <div class='top'>
            <div class='ls-top'>
                <h3>{{ shortenString(postData.title, 25) }}</h3>
                <p style='white-space: pre-line;'>{{ shortenString(postData.body, 200, 2) }}</p>
            </div>

            <div class='rs-top' v-if='postData.photos.length > 0'>
                <!-- <img :src='postData.photos[0]!.image_src' /> -->
                <div
                    class='img-wrapper'
                    :style='{backgroundImage: `url(postData.photos[0]!.image_src)`}'
                ></div>
            </div>
        </div>

        <div class='bottom'>

        </div>
    </div>
</template>

<style>
@import url('./ProfilePostView.css');
</style>