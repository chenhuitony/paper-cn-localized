package org.bukkit.material;

import org.bukkit.Material;
import org.bukkit.TreeSpecies;

/**
 * Represents wood blocks of different species.
 *
 * @see Material#LEGACY_WOOD
 * @see Material#LEGACY_SAPLING
 * @see Material#LEGACY_WOOD_DOUBLE_STEP
 *
 * @deprecated all usage of MaterialData is deprecated and subject to removal.
 * Use {@link org.bukkit.block.data.BlockData}.
 */
@Deprecated(since = "1.13", forRemoval = true)
public class Wood extends MaterialData {
    protected static final Material DEFAULT_TYPE = Material.LEGACY_WOOD;
    protected static final TreeSpecies DEFAULT_SPECIES = TreeSpecies.GENERIC;

    /**
     * Constructs a wood block.
     */
    public Wood() {
        this(DEFAULT_TYPE, DEFAULT_SPECIES);
    }

    /**
     * Constructs a wood block of the given tree species.
     *
     * @param species the species of the wood block
     */
    public Wood(TreeSpecies species) {
        this(DEFAULT_TYPE, species);
    }

    /**
     * Constructs a wood block of the given type.
     *
     * @param type the type of wood block
     */
    public Wood(final Material type) {
        this(type, DEFAULT_SPECIES);
    }

    /**
     * Constructs a wood block of the given type and tree species.
     *
     * @param type the type of wood block
     * @param species the species of the wood block
     */
    public Wood(final Material type, final TreeSpecies species) {
        // Ensure only valid species-type combinations
        super(getSpeciesType(type, species));
        setSpecies(species);
    }

    /**
     * @param type the type
     * @param data the raw data value
     * @deprecated Magic value
     */
    @Deprecated(since = "1.9")
    public Wood(final Material type, final byte data) {
        super(type, data);
    }

    /**
     * Gets the current species of this wood block
     *
     * @return TreeSpecies of this wood block
     */
    public TreeSpecies getSpecies() {
        switch (getItemType()) {
            case LEGACY_WOOD:
            case LEGACY_WOOD_DOUBLE_STEP:
                return TreeSpecies.getByData((byte) getData());
            case LEGACY_LOG:
            case LEGACY_LEAVES:
                return TreeSpecies.getByData((byte) (getData() & 0x3));
            case LEGACY_LOG_2:
            case LEGACY_LEAVES_2:
                return TreeSpecies.getByData((byte) ((getData() & 0x3) | 0x4));
            case LEGACY_SAPLING:
            case LEGACY_WOOD_STEP:
                return TreeSpecies.getByData((byte) (getData() & 0x7));
            default:
                throw new IllegalArgumentException("树种的方块类型无效");
        }
    }

    /**
     * Correct the block type for certain species-type combinations.
     *
     * @param type The desired type
     * @param species The required species
     * @return The actual type for this species given the desired type
     */
    private static Material getSpeciesType(Material type, TreeSpecies species) {
        switch (species) {
            case GENERIC:
            case REDWOOD:
            case BIRCH:
            case JUNGLE:
                switch (type) {
                    case LEGACY_LOG_2:
                        return Material.LEGACY_LOG;
                    case LEGACY_LEAVES_2:
                        return Material.LEGACY_LEAVES;
                    default:
                }
                break;
            case ACACIA:
            case DARK_OAK:
                switch (type) {
                    case LEGACY_LOG:
                        return Material.LEGACY_LOG_2;
                    case LEGACY_LEAVES:
                        return Material.LEGACY_LEAVES_2;
                    default:
                }
                break;
        }
        return type;
    }

    /**
     * Sets the species of this wood block
     *
     * @param species New species of this wood block
     */
    public void setSpecies(final TreeSpecies species) {
        boolean firstType = false;
        switch (getItemType()) {
            case LEGACY_WOOD:
            case LEGACY_WOOD_DOUBLE_STEP:
                setData(species.getData());
                break;
            case LEGACY_LOG:
            case LEGACY_LEAVES:
                firstType = true;
            // fall through to next switch statement below
            case LEGACY_LOG_2:
            case LEGACY_LEAVES_2:
                switch (species) {
                    case GENERIC:
                    case REDWOOD:
                    case BIRCH:
                    case JUNGLE:
                        if (!firstType) {
                            throw new IllegalArgumentException("block type 的树木种类无效，请改用 block type 2");
                        }
                        break;
                    case ACACIA:
                    case DARK_OAK:
                        if (firstType) {
                            throw new IllegalArgumentException("block type 2 的树木种类无效，请改用 block type");
                        }
                        break;
                }
                setData((byte) ((getData() & 0xC) | (species.getData() & 0x3)));
                break;
            case LEGACY_SAPLING:
            case LEGACY_WOOD_STEP:
                setData((byte) ((getData() & 0x8) | species.getData()));
                break;
            default:
                throw new IllegalArgumentException("树种的方块类型无效");
        }
    }

    @Override
    public String toString() {
        return getSpecies() + " " + super.toString();
    }

    @Override
    public Wood clone() {
        return (Wood) super.clone();
    }
}
