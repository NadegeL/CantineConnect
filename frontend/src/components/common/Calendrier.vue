<template>
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Gestion Calendrier</h1>
        <CalendrierCantine />
    </div>
</template>

<script>
import CalendrierCantine from '@/components/common/CalendrierCantine.vue';

export default {
    components: {
        CalendrierCantine
    }
}
</script>