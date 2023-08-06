import PiecesCacheSingleton from '../cache/pieces_cache';
import ConnectorSingleton from './connector_singleton';
import { drawSnippets } from '../ui/piecesView';
import versionCheck from './version_check';

const config = ConnectorSingleton.getInstance();
const cache = PiecesCacheSingleton.getInstance();

let intervalId: NodeJS.Timeout[] = [];
export default async function pollForNewSnippets(): Promise<void> {
    intervalId.forEach((id) => clearInterval(id));
    intervalId = [];
    const check = await versionCheck({ minVersion: '5.0.1' });
    intervalId.push(
        setInterval(
            async () => {
                const snapshot = check
                    ? await config.assetsApi.assetsIdentifiersSnapshot()
                    : await config.assetsApi.assetsSnapshot({
                          transferables: false,
                          suggested: false,
                      });
                if (!snapshot.iterable) return;
                for (const asset of snapshot.iterable) {
                    if (!cache.mappedAssets[asset.id]) {
                        const newAsset = await config.assetApi.assetSnapshot({
                            asset: asset.id,
                            transferables: true,
                        });

                        cache.prependAsset({ asset: newAsset });
                        drawSnippets({});
                    }
                }
            },
            check ? 10_000 : 300_000
        )
    );
}

export function stopPolling() {
    intervalId.forEach((id) => clearInterval(id));
    intervalId = [];
}
