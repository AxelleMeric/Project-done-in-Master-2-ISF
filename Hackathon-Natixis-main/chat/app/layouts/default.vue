<template>
  <main class="h-screen flex flex-col">
    <UHeader class="sticky top-0 z-50 shrink-0">
      <template #title>
        <div class="flex justify-center items-center gap-2">
          <img src="/favicon.png" alt="Natixis Logo" class="h-8 object-contain">
          <h3>
            Natixis <span class="text-primary">Chat</span>
          </h3>
        </div>
      </template>
      <template #right>
        <div class="flex items-center gap-2">
          <Helper />
          <UColorModeButton variant="soft" />
        </div>
      </template>
    </UHeader>
    <!-- <div class="pointer-events-none fixed inset-0 z-0 size-full overflow-hidden">
      <div class="pointer-events-none absolute inset-[-200%] z-0 size-[400%] opacity-30" style="background: radial-gradient(circle at 50% 50%, rgba(128, 0, 255, 0.4) 0%, rgba(180, 100, 255, 0.2) 25%, transparent 60%);" />
    </div> -->
    <div class="relative z-10 h-[calc(100vh-4rem)] mt-16">
      <slot />
    </div>
  </main>
</template>
