import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'
import ts from 'typescript'

const source = readFileSync(new URL('../src/utils/analysisModels.ts', import.meta.url), 'utf8')
const { outputText } = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.ESNext } })
const { configuredAnalysisModels, selectAvailableModel, hasSelectedModels } =
  await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`)

test('only enabled models with an enabled, configured provider can be selected', () => {
  const providers = [
    { name: 'deepseek', display_name: 'DeepSeek', is_active: true, extra_config: { has_api_key: true } },
    { name: 'openai', is_active: true, extra_config: { has_api_key: false } },
    { name: 'qwen', is_active: false, extra_config: { has_api_key: true } }
  ]
  const models = [
    { model_name: 'deepseek-chat', provider: 'deepseek', enabled: true },
    { model_name: 'disabled', provider: 'deepseek', enabled: false },
    { model_name: 'gpt', provider: 'openai', enabled: true },
    { model_name: 'qwen-turbo', provider: 'dashscope', enabled: true },
    { model_name: ' ', provider: 'deepseek', enabled: true }
  ]
  const options = configuredAnalysisModels(models, providers)
  assert.deepEqual(options.map(m => m.model_name), ['deepseek-chat'])
  assert.equal(selectAvailableModel(options, 'qwen-turbo'), 'deepseek-chat')
  assert.equal(hasSelectedModels(options, 'deepseek-chat', 'qwen-max'), false)
  assert.equal(hasSelectedModels(options, 'deepseek-chat', 'deepseek-chat'), true)
})

test('provider aliases and legacy masked credential metadata are supported', () => {
  const models = [{ model_name: 'qwen-plus', provider: 'dashscope', enabled: true }]
  assert.equal(configuredAnalysisModels(models, [{ name: 'qwen', is_active: true, api_key: 'masked' }]).length, 1)
  assert.equal(configuredAnalysisModels(models, [{ name: 'qwen', is_active: true, api_key: 'masked', extra_config: { has_api_key: false } }]).length, 0)
})

test('empty configuration never falls back to an unconfigured model', () => {
  assert.equal(selectAvailableModel([], 'qwen-turbo'), '')
  assert.equal(hasSelectedModels([], '', ''), false)
})

test('ambiguous model IDs cannot silently select another provider', () => {
  const models = ['openai', 'openrouter'].map(provider => ({ provider, model_name: 'same-id', enabled: true }))
  const providers = models.map(m => ({ name: m.provider, is_active: true, extra_config: { has_api_key: true } }))
  assert.equal(configuredAnalysisModels(models, providers).length, 0)
})
