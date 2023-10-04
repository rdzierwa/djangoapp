// static/main.js
function openAddProductModal() {
    $('#productModal').modal('show');
  }
function addProduct() {
    // Otwórz modal
    $('#productModal').modal('show');
  }
  
  function submitProduct() {
    // Pobieranie wartości z formularza
    const idShoper = document.getElementById('id_shoper').value;
    const sku = document.getElementById('sku').value;
    const ean = document.getElementById('ean').value;
    const qty = document.getElementById('qty').value;
    const synchronization = document.getElementById('synchronization').value;
    const updateDate = document.getElementById('update_date').value;
    
    // Utworzenie obiektu z danymi formularza
    const productData = {
        id_shoper: idShoper,
        sku: sku,
        ean: ean,
        qty: qty,
        synchronization: synchronization,
        update_date: updateDate
    };
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Wysłanie danych do serwera
    axios.post('api/product/add_product/', productData, {
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        // Przetwarzanie odpowiedzi od serwera
        console.log('Produkt dodany pomyślnie: ', response.data);
        // Zamknięcie modalu
        $('#productModal').modal('hide');
        window.location.reload();
    })
    .catch(error => {
        // Obsługa błędów
        console.error('Błąd podczas dodawania produktu: ', error);
    });
}



function synchronizeProduct(productId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    axios.post(`api/product/${productId}/synchronize/`,{},{
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
        .then(response => {
            // Zaktualizuj status synchronizacji produktu w tabeli
            const syncStatus = response.data.synchronization ? 'True' : 'False';
            document.getElementById(`product-${productId}-synchronization`).innerText = syncStatus;
        })
        .catch(error => {
            console.error('Error during product synchronization', error);
        });
}

function deleteProduct(productId, element) {
    const userConfirmed = confirm('Czy na pewno chcesz usunąć ten produkt?');
    if(!userConfirmed) return;
    
    const currentPage = element.dataset.currentPage;
    const maxPage = element.dataset.maxPage;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    axios.delete(`product/${productId}/delete/`, {headers: {'X-CSRFToken': csrfToken}})
    .then(response => {
        if(currentPage < maxPage) {
            window.location.href = `?page=${currentPage}`;
        } else if(currentPage > 1) {
            window.location.href = `?page=${currentPage - 1}`;
        } else {
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error while deleting the product', error);
    });
}




