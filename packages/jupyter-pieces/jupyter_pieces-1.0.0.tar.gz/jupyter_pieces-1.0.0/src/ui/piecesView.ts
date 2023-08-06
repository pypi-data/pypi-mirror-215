import { JupyterFrontEnd } from '@jupyterlab/application';
import { Widget } from '@lumino/widgets';
import { returnedSnippet } from '../typedefs';
import PiecesCacheSingleton from '../cache/pieces_cache';
import { loadPieces, processAssets } from '../connection/api_wrapper';
import { search } from '../actions/search';
import createAsset from './../actions/create_asset';
import { LabIcon } from '@jupyterlab/ui-components';
import Constants from '../const';
import { showLoadingState } from './render/showLoadingState';
import { showNoSnippetState } from './render/showNoSnippetState';
import { showLoadErrorState } from './render/showLoadErrorState';
import { renderListView } from './views/renderListView';
import { renderLanguageView } from './views/renderLanguageView';
import { renderLoading } from './render/renderSnippets';
import { SegmentAnalytics } from '../analytics/SegmentAnalytics';
import { AnalyticsEnum } from '../analytics/AnalyticsEnum';

export enum SortSnippetsBy {
    Recent,
    Language,
}

export let isLoading = true;
let isFetchFailed = false;
let defaultSortingView = SortSnippetsBy.Recent;
let curSnippets: returnedSnippet[] = [];

export function setIsLoading(val: boolean) {
    isLoading = val;
}

export function setIsFetchFailed(val: boolean) {
    isFetchFailed = val;
}

export function setDefaultSortingView(val: SortSnippetsBy) {
    defaultSortingView = val;
}

const piecesContainer = document.createElement('div');
const containerDiv = document.createElement('div');
const cache: PiecesCacheSingleton = PiecesCacheSingleton.getInstance();

export class PiecesView {
    private app: any;
    private viewWidget!: Widget;
    private defaultSearchQuery: string = '';
    private searchBtn = document.createElement('button');
    private searchBox = document.createElement('input');

    private refreshIcon = new LabIcon({
        name: 'jupyter-pieces:refresh',
        svgstr: Constants.REFRESH_SVG,
    });

    private cancelIcon = new LabIcon({
        name: 'jupyter-pieces:cancel',
        svgstr: Constants.CANCEL_SVG,
    });

    private searchCancelled = false;

    public build(app: JupyterFrontEnd): void {
        this.app = app;

        this.createView();
        this.prepareRightClick();
    }

    private saveSelection(): void {
        console.log('Saving: ' + this.app.Editor.selection);
        SegmentAnalytics.track({
            event: AnalyticsEnum.JUPYTER_SAVE_SELECTION,
        });
        createAsset(this.app.Editor.selection);
    }

    private prepareRightClick(): void {
        const command = 'jupyter-pieces:menuitem';

        this.app.commands.addCommand(command, {
            label: 'Save to Pieces',
            execute: this.saveSelection,
        });

        this.app.contextMenu.addItem({
            command: command,
            selector: '.jp-CodeCell-input .jp-Editor .jp-Notebook *',
            rank: 100,
        });
    }

    private async handleSearch({ query }: { query: string }): Promise<void> {
        if (query === '' || this.defaultSearchQuery === query) {
            return;
        }
        this.defaultSearchQuery = query;
        const result = await search({ query: query });
        if (this.searchCancelled) {
            this.searchCancelled = false;
            return;
        }
        await drawSnippets({ snippets: result });
    }

    private searchBoxElement(): HTMLElement {
        const searchRow = document.createElement('div');
        searchRow.classList.add('row', 'search-row');

        const inputCol = document.createElement('div');
        inputCol.classList.add('col');
        const searchBox = this.searchBox;
        searchBox.classList.add('search-input', 'jp-input');
        searchBox.type = 'text';
        searchBox.placeholder = '🔍  Search for Snippets...';
        searchBox.value = this.defaultSearchQuery;

        inputCol.appendChild(searchBox);
        searchRow.appendChild(inputCol);

        const searchBtnCol = document.createElement('div');
        searchBtnCol.classList.add('col');
        searchBtnCol.classList.add('col-sm');
        const searchBtn = this.searchBtn;
        searchBtn.title = 'Refresh snippets';
        searchBtn.classList.add('pieces-btn-search', 'jp-btn');
        this.defaultSearchQuery === ''
            ? this.refreshIcon.element({ container: searchBtn })
            : this.cancelIcon.element({ container: searchBtn });
        searchBtn.addEventListener('click', async () => {
            if (this.defaultSearchQuery === '') {
                this.defaultSearchQuery = '';

                SegmentAnalytics.track({
                    event: AnalyticsEnum.JUPYTER_REFRESH_CLICKED,
                });

                const loading = renderLoading(document, 'refresh-');
                searchBtnCol.replaceChild(loading, searchBtn);
                try {
                    await loadPieces();
                    drawSnippets({});
                } catch (e) {
                    console.log(e);
                }
                searchBtnCol.replaceChild(searchBtn, loading);
            } else {
                this.defaultSearchQuery = '';
                // this.searchCancelled = true; // TODO ADD LOGIC FOR CANCEL
                this.searchBox.value = '';
                this.refreshIcon.element({ container: searchBtn });
                searchBtn.title = 'Refresh snippets';
                drawSnippets({});
            }
        });

        searchBox.addEventListener('keyup', async (event) => {
            if (event.key === 'Enter' && searchBox.value != '') {
                const loading = renderLoading(document, 'refresh-');
                searchBtnCol.replaceChild(loading, searchBtn);
                try {
                    await this.handleSearch({ query: searchBox.value });
                    this.cancelIcon.element({ container: this.searchBtn });
                    searchBtn.title = 'Clear Search';
                } catch (e) {
                    console.log(e);
                }
                searchBtnCol.replaceChild(searchBtn, loading);
            }
        });
        searchBtnCol.appendChild(searchBtn);
        searchRow.appendChild(searchBtnCol);

        return searchRow;
    }

    private sortSnippetsDropdownElement(): HTMLElement {
        const dropdownRow = document.createElement('div');
        dropdownRow.classList.add('row', 'search-row');

        const dropdownElement = document.createElement('select');
        dropdownElement.classList.add('jp-dropdown');

        const option_recent = document.createElement('option');
        option_recent.value = 'recent';
        option_recent.innerText = '🕓 RECENT';
        dropdownElement.appendChild(option_recent);

        const option_language = document.createElement('option');
        option_language.value = 'language';
        option_language.innerText = '🌐 LANGUAGE';
        dropdownElement.appendChild(option_language);

        const option_arrow = document.createElement('span');
        option_arrow.innerText = '▼';
        option_arrow.classList.add('jp-dropdown-arrow');

        dropdownElement.addEventListener('change', () => {
            if (dropdownElement.value === 'language') {
                setDefaultSortingView(SortSnippetsBy.Language);
            } else if (dropdownElement.value === 'recent') {
                setDefaultSortingView(SortSnippetsBy.Recent);
            }
            console.log(this.defaultSearchQuery);
            if (this.defaultSearchQuery === '') {
                drawSnippets({});
            } else {
                drawSnippets({ snippets: curSnippets });
            }
        });

        dropdownRow.appendChild(dropdownElement);
        dropdownRow.appendChild(option_arrow);

        return dropdownRow;
    }

    // This should only be called once.
    private createView() {
        // Create and activate your view widget
        const viewWidget = new Widget();
        const PiecesLogo = new LabIcon({
            name: 'jupyter-pieces:logo',
            svgstr: Constants.PIECES_LOGO,
        });
        viewWidget.id = 'piecesView';
        viewWidget.title.closable = true;
        viewWidget.title.icon = PiecesLogo;
        this.viewWidget = viewWidget;

        //Add the search box
        piecesContainer.id = 'piecesContainer';
        piecesContainer.classList.add('pieces-container');
        this.viewWidget.node.appendChild(piecesContainer);
        const searchBoxDiv = document.createElement('div');
        searchBoxDiv.classList.add('search-box-div');
        searchBoxDiv.appendChild(this.searchBoxElement());
        searchBoxDiv.appendChild(this.sortSnippetsDropdownElement());

        piecesContainer.appendChild(searchBoxDiv);

        this.app.shell.add(this.viewWidget, 'right', { rank: 1 });

        drawSnippets({});
        piecesContainer.appendChild(containerDiv);
        containerDiv.classList.add('container-div');
    }
}

// Make sure you call create view before calling this
//   - this is also called by createview
// Call this to redraw the view
export async function drawSnippets({
    snippets,
}: {
    snippets?: returnedSnippet[];
}) {
    containerDiv.innerHTML = '';
    containerDiv.classList.remove('load-error-state');

    //Set up the loading state
    if (isLoading) {
        showLoadingState(containerDiv);
        return;
    }

    if (isFetchFailed) {
        showLoadErrorState(containerDiv);
        return;
    }

    if (cache.assets.length === 0) {
        showNoSnippetState(containerDiv);
        return;
    }

    let piecesSnippets =
        snippets !== undefined
            ? snippets
            : (
                  await processAssets({
                      assets: cache.assets,
                  })
              ).snippets;

    curSnippets = piecesSnippets;

    if (defaultSortingView === SortSnippetsBy.Recent) {
        renderListView({
            container: containerDiv,
            snippets: piecesSnippets.sort(
                (a, b) => b.created.getTime() - a.created.getTime()
            ),
        });
    } else if (defaultSortingView === SortSnippetsBy.Language) {
        renderLanguageView({
            container: containerDiv,
            snippets: piecesSnippets.sort((a, b) =>
                a.language.localeCompare(b.language)
            ),
        });
    }
}
