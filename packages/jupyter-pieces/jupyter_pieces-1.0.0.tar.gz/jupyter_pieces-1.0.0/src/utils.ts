import { parseDescription } from './ui/utils/parseDescription';
import ConnectorSingleton from './connection/connector_singleton';
import PiecesCacheSingleton from './cache/pieces_cache';

export const timeoutPromise: (duration: number) => Promise<void> = (
    duration: number
): Promise<void> => new Promise((resolver) => setTimeout(resolver, duration));

export const isDateLessThan15MinutesOld = (date: Date) => {
    const currentTime = new Date();
    const timeDifference = currentTime.getTime() - date.getTime();
    const minutesDifference = Math.floor(timeDifference / 1000 / 60);

    return minutesDifference < 15;
};

/*
	Use this function to poll POS for an updated description and title
	This is necessary as it takes some time to generate, and we don't
	want to hang the UI. 
	
	This does not cause a rerender, as it only updates
	the inner text of the 'title' and 'description' elements that are
	already rendered for that snippet.
*/
export const pollAndUpdateSnippetDesc = async ({
    descEl,
    snippetId,
    created,
    titleEl,
}: {
    descEl: HTMLElement;
    snippetId: string;
    created: Date;
    titleEl: HTMLElement;
}): Promise<void> => {
    await sleep(1000);
    const config = ConnectorSingleton.getInstance();
    let descUpdated = false;
    while (!descUpdated && isDateLessThan15MinutesOld(created)) {
        const snapshot = await config.assetApi.assetSnapshot({
            asset: snippetId,
            transferables: false,
        });
        if (
            snapshot.name &&
            snapshot.description &&
            snapshot.description !==
                '📝 Custom Description: \nWrite a custom description here.'
        ) {
            descUpdated = true;
            descEl.innerText = parseDescription(snapshot.description);
            titleEl.innerText = snapshot.name;
            const storage = PiecesCacheSingleton.getInstance();

            // update the storage singleton
            for (let i = 0; i < storage.assets.length; i++) {
                if (storage.assets[i].id === snippetId) {
                    storage.assets[i].description = snapshot.description;
                    storage.assets[i].name = snapshot.name;
                }
            }

            return;
        }
        await sleep(3000);
    }
};

export const PromiseResolution: {
    <T>(): {
        resolver: { (args: T): T | void };
        rejector: { (args: T): T | void };
        promise: Promise<T>;
    };
} = <T>() => {
    let resolver!: { (args: T): T | void };
    let rejector!: { (args: T): T | void };

    const promise: Promise<T> = new Promise<T>(
        (resolve: { (args: T): T | void }) => {
            resolver = (args: T) => resolve(args);
            rejector = (args: T) => resolve(args);
        }
    );
    return {
        promise,
        resolver,
        rejector,
    };
};

async function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
