<!-- 系统设置 - 占位页 -->
<!-- @author fortune -->
<!-- @date 2026-03-18 21:55:00 -->

<template>
  <div class="p-6 animate-fade-in">
    <div class="glass-card p-8">
      <h2 class="text-lg font-semibold mb-4 text-[var(--dp-text-primary)]">系统设置</h2>
      <p class="text-sm mb-4 text-[var(--dp-text-muted)]">
        API Key 等配置请通过项目根目录的 .env 文件设置。
      </p>
      <div class="space-y-2 text-xs text-[var(--dp-text-muted)]">
        <p>DASHSCOPE_API_KEY - 通义千问 API Key</p>
        <p>DASHSCOPE_MODEL - 模型名称（默认 qwen3.5-plus）</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 系统设置占位页
</script>
