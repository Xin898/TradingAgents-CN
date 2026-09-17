import type { LLMConfig, LLMProvider } from '@/api/config'

const aliases: Record<string, string> = {
  dashscope: 'qwen', alibaba: 'qwen', zhipu: 'glm', baidu: 'qianfan'
}
export const providerKey = (name: string) => aliases[name] || name

export function configuredAnalysisModels(models: LLMConfig[], providers: LLMProvider[]) {
  const ready = new Map(providers.filter(p => p.is_active &&
    (p.extra_config?.has_api_key ?? Boolean(p.api_key)))
    .map(p => [providerKey(p.name), p]))
  // The analysis API resolves providers by model name. Ambiguous names must not
  // silently route a selection to another configured provider.
  const owners = new Map<string, Set<string>>()
  for (const model of models) {
    const name = model.model_name?.trim()
    if (!name) continue
    const set = owners.get(name) || new Set<string>()
    set.add(providerKey(model.provider))
    owners.set(name, set)
  }
  return models.filter(m => m.enabled && m.model_name?.trim() &&
    ready.has(providerKey(m.provider)) && owners.get(m.model_name.trim())?.size === 1)
    .map(m => ({ ...m, model_name: m.model_name.trim(),
      provider: providerKey(m.provider),
      provider_display_name: ready.get(providerKey(m.provider))!.display_name }))
}

export function selectAvailableModel(models: { model_name: string }[], preferred?: string) {
  return models.find(m => m.model_name === preferred)?.model_name || models[0]?.model_name || ''
}

export function hasSelectedModels(models: { model_name: string }[], quick: string, deep: string) {
  return Boolean(quick && deep && models.some(m => m.model_name === quick) &&
    models.some(m => m.model_name === deep))
}
