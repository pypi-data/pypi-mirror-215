import ConnectorSingleton from '../connection/connector_singleton';
import {
    AssetReclassification,
    AssetReclassifyRequest,
} from '../PiecesSDK/core';
import { ClassificationSpecificEnum } from '../PiecesSDK/connector';
import { Asset } from '../PiecesSDK/common/models/Asset';
import Notifications from '../connection/notification_handler';
import Constants from '../const';
import { SegmentAnalytics } from '../analytics/SegmentAnalytics';
import { AnalyticsEnum } from '../analytics/AnalyticsEnum';

const config = ConnectorSingleton.getInstance();
const notifications = Notifications.getInstance();

export const reclassify = async ({
    asset,
    ext,
}: {
    asset: Asset;
    ext: ClassificationSpecificEnum;
}): Promise<Asset | void> => {
    try {
        const reclassification: AssetReclassification = {
            asset: asset,
            ext: ext,
        };
        const params: AssetReclassifyRequest = {
            assetReclassification: reclassification,
            transferables: false,
        };
        const ret: Asset = await config.assetApi.assetReclassify(params);
        notifications.information({ message: Constants.RECLASSIFY_SUCCESS });
        return ret;
    } catch (error) {
        console.error(error);
        notifications.error({ message: Constants.RECLASSIFY_FAILURE });
        return;
    }
};

export const update = async ({
    asset,
}: {
    asset: Asset;
}): Promise<Asset | void> => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_EDIT_SNIPPET,
    });

    try {
        const ret: Asset = await config.assetApi.assetUpdate({ asset: asset });
        notifications.information({ message: Constants.UPDATE_SUCCESS });
        return ret;
    } catch (error) {
        console.error(error);
        notifications.error({ message: Constants.UPDATE_FAILURE });
        return;
    }
};
