# Agents Instructions

## Tools

Use `mise x --` prefix for any tool managed by mise (e.g., `bun`). This is required because the shell is non-interactive and doesn't source ~/.bashrc.

For Python dependencies, use `uv pip install --system` instead of `pip install`.

Example:
```bash
mise x -- bun install
mise x -- bun run dev
mise x -- bun run build
```

## Frontend

The frontend uses Vue 3 + Vite + TypeScript with Tidewave integration. 

**Styling:**
- The project uses Tailwind CSS v4.
- Prefer Tailwind utility classes over custom CSS.
- Configure theme variables in `src/style.css` using the `@theme` block.
- Use `@apply` in `src/style.css` only when necessary for base element styling.

Commands:
- `mise x -- bun run dev` - Start dev server
- `mise x -- bun run build` - Build to `dist/`
- `mise x -- bun run preview` - Preview production build

## Mise Tasks

- `mise run server` - Start the frontend dev server
