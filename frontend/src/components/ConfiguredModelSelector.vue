<template>
  <div class="configured-model-selector">
    <el-select v-model="provider" placeholder="选择已配置的厂家" size="small"
      style="width: 100%" :disabled="!providers.length" @change="changeProvider">
      <el-option v-for="item in providers" :key="item.name" :label="item.label" :value="item.name" />
    </el-select>
    <el-select :model-value="modelValue" placeholder="选择模型" size="small" filterable
      style="width: 100%; margin-top: 8px" :disabled="!models.length"
      @update:model-value="emit('update:modelValue', $event)">
      <el-option v-for="model in models" :key="model.model_name"
        :label="model.model_display_name || model.model_name" :value="model.model_name" />
    </el-select>
    <p v-if="!providers.length" class="empty-models">
      暂无可用模型。请在配置管理中配置厂家密钥，并启用厂家及模型。
      <router-link to="/settings/config">前往配置</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { LLMConfig } from '@/api/config'

const props = defineProps<{
  modelValue: string
  availableModels: (LLMConfig & { provider_display_name?: string })[]
}>()
const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()
const provider = ref('')
const providers = computed(() => Array.from(new Map(props.availableModels.map(m =>
  [m.provider, { name: m.provider, label: m.provider_display_name || m.provider }])).values()))
const models = computed(() => props.availableModels.filter(m => m.provider === provider.value))
watch(() => [props.modelValue, props.availableModels] as const, () => {
  provider.value = props.availableModels.find(m => m.model_name === props.modelValue)?.provider || ''
}, { immediate: true })
const changeProvider = () => emit('update:modelValue', models.value[0]?.model_name || '')
</script>

<style scoped>
.empty-models { color: var(--el-text-color-secondary); font-size: 12px; line-height: 1.6; }
</style>
