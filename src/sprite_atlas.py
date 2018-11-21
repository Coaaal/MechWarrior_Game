def get_sprite_atlas(tile_dimension):
    return {
            "PLAYER_HUMAN": [(1 * int(tile_dimension)), (0 * tile_dimension),
                             tile_dimension, tile_dimension],
            "DESSERT": [(0 * tile_dimension), (0 * tile_dimension),
                        tile_dimension, tile_dimension],
            "PLACEHOLDER": [(3 * tile_dimension), (1 * tile_dimension),
                            tile_dimension, tile_dimension],
            "WEAPON": [(2 * tile_dimension), (0 * tile_dimension),
                       tile_dimension, tile_dimension],
            "WALL": [(0 * tile_dimension), (1 * tile_dimension),
                     tile_dimension, tile_dimension],
            "POWER_UP": [(2 * tile_dimension), (1 * tile_dimension),
                         tile_dimension, tile_dimension],
            "BULLET": [(2 * tile_dimension), (1 * tile_dimension),
                       tile_dimension, tile_dimension]
        }


def get_explosion_atlas(tile_dimension):
    return {
        "FRAMES": {
            0: [(0 * tile_dimension), (0 * tile_dimension), tile_dimension, tile_dimension],
            1: [(1 * tile_dimension), (0 * tile_dimension), tile_dimension, tile_dimension],
            2: [(2 * tile_dimension), (0 * tile_dimension), tile_dimension, tile_dimension],
            3: [(3 * tile_dimension), (0 * tile_dimension), tile_dimension, tile_dimension],
            4: [(4 * tile_dimension), (0 * tile_dimension), tile_dimension, tile_dimension],
            5: [(5 * tile_dimension), (0 * tile_dimension), tile_dimension, tile_dimension],
            6: [(6 * tile_dimension), (0 * tile_dimension), tile_dimension, tile_dimension],
            7: [(7 * tile_dimension), (0 * tile_dimension), tile_dimension, tile_dimension]
        }
    }
