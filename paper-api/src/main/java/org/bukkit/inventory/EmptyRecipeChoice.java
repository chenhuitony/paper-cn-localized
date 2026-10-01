package org.bukkit.inventory;

import org.jetbrains.annotations.ApiStatus;
import org.jspecify.annotations.NullMarked;

@ApiStatus.Internal
@NullMarked
record EmptyRecipeChoice() implements RecipeChoice {

    static final RecipeChoice INSTANCE = new EmptyRecipeChoice();
    @Override
    @Deprecated(since = "1.13.1")
    public ItemStack getItemStack() {
        throw new UnsupportedOperationException("这是一个空的 RecipeChoice");
    }

    @SuppressWarnings("MethodDoesntCallSuperMethod")
    @Override
    public RecipeChoice clone() {
        return this;
    }

    @Override
    public boolean test(final ItemStack itemStack) {
        return false;
    }

    @Override
    public RecipeChoice validate(final boolean allowEmptyRecipes) {
        if (allowEmptyRecipes) return this;
        throw new IllegalArgumentException("空的 RecipeChoice 在此处不被允许");
    }
}
