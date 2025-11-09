import { useState, useEffect } from 'react';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  categories: Category[];
  tags: Tag[];
}

interface Category {
  id: number;
  name: string;
}

interface Tag {
  id: number;
  name: string;
}

export default function App() {
  const API_BASE_URL_DEV = 'http://localhost:8000/api/';
  const PRODUCTS_RESOURCE = 'products/';
  const CATEGORY_RESOURCE = 'categories/';
  const TAGS_RESOURCE = 'tags/';

  const [products, setProducts] = useState<Product[]>([]);
  const [allCategories, setAllCategories] = useState<Category[]>([]);
  const [allTags, setAllTags] = useState<Tag[]>([]);
  const [searchText, setSearchText] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<number[]>([]);
  const [selectedTags, setSelectedTags] = useState<number[]>([]);
  const [categoryDropdown, setCategoryDropdown] = useState<string>('');
  const [tagDropdown, setTagDropdown] = useState<string>('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [productsRes, categoriesRes, tagsRes] = await Promise.all([
        fetch(`${API_BASE_URL_DEV}${PRODUCTS_RESOURCE}`).then(r => r.json()),
        fetch(`${API_BASE_URL_DEV}${CATEGORY_RESOURCE}`).then(r => r.json()),
        fetch(`${API_BASE_URL_DEV}${TAGS_RESOURCE}`).then(r => r.json()),
      ]);

      setProducts(productsRes);
      setAllCategories(categoriesRes);
      setAllTags(tagsRes);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const filterData = async () => {
    try {
      const params = new URLSearchParams();
      if (searchText) params.append('search', searchText);
      if (selectedCategories.length) params.append('category', selectedCategories.join(','));
      if (selectedTags.length) params.append('tag', selectedTags.join(','));

      const response = await fetch(`${API_BASE_URL_DEV}${PRODUCTS_RESOURCE}?${params}`);
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error filtering data:', error);
    }
  };

  const addCategory = () => {
    const categoryId = parseInt(categoryDropdown);
    if (categoryId && !selectedCategories.includes(categoryId)) {
      setSelectedCategories([...selectedCategories, categoryId]);
    }
    setCategoryDropdown('');
  };

  const addTag = () => {
    const tagId = parseInt(tagDropdown);
    if (tagId && !selectedTags.includes(tagId)) {
      setSelectedTags([...selectedTags, tagId]);
    }
    setTagDropdown('');
  };

  const handleDeleteCategory = (categoryId: number) => {
    setSelectedCategories(prev => prev.filter(id => id !== categoryId));
  };

  const handleDeleteTag = (tagId: number) => {
    setSelectedTags(prev => prev.filter(id => id !== tagId));
  };

  return (
    <div>
      <h1>Product Inventory</h1>
      
      <div>
        <div>
          <label>Search:</label>
          <input
            type="text"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="Search descriptions..."
          />
        </div>

        <div>
          <label>Add Category:</label>
          <select
            value={categoryDropdown}
            onChange={(e) => setCategoryDropdown(e.target.value)}
          >
            <option value="">-- Select Category --</option>
            {allCategories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
          <button onClick={addCategory}>Add</button>
          
          <div>
            <strong>Selected Categories:</strong>
            {selectedCategories.length === 0 ? (
              <span> None</span>
            ) : (
              selectedCategories.map((id) => {
                const cat = allCategories.find((c) => c.id === id);
                return cat ? (
                  <span key={id}>
                    {' '}[{cat.name}]
                    <button onClick={() => handleDeleteCategory(id)}>×</button>
                  </span>
                ) : null;
              })
            )}
          </div>
        </div>

        <div>
          <label>Add Tag:</label>
          <select
            value={tagDropdown}
            onChange={(e) => setTagDropdown(e.target.value)}
          >
            <option value="">-- Select Tag --</option>
            {allTags.map((tag) => (
              <option key={tag.id} value={tag.id}>
                {tag.name}
              </option>
            ))}
          </select>
          <button onClick={addTag}>Add</button>
          
          <div>
            <strong>Selected Tags:</strong>
            {selectedTags.length === 0 ? (
              <span> None</span>
            ) : (
              selectedTags.map((id) => {
                const tag = allTags.find((t) => t.id === id);
                return tag ? (
                  <span key={id}>
                    {' '}[{tag.name}]
                    <button onClick={() => handleDeleteTag(id)}>×</button>
                  </span>
                ) : null;
              })
            )}
          </div>
        </div>

        <div>
          <button onClick={filterData}>Filter</button>
        </div>
      </div>

      <div>
        <table border={1}>
          <thead>
            <tr>
              <th>Product Name</th>
              <th>Description</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Categories</th>
              <th>Tags</th>
            </tr>
          </thead>
          <tbody>
            {products.length === 0 ? (
              <tr>
                <td colSpan={6}>No products found</td>
              </tr>
            ) : (
              products.map((product) => (
                <tr key={product.id}>
                  <td>{product.name}</td>
                  <td>
                    {product.description || <em>No description</em>}
                  </td>
                  <td>${parseFloat(product.price.toString()).toFixed(2)}</td>
                  <td>{product.stock}</td>
                  <td>
                    {product.categories && product.categories.length > 0 ? (
                      product.categories.map((category) => (
                        <span key={category.id}>[{category.name}] </span>
                      ))
                    ) : (
                      <span>None</span>
                    )}
                  </td>
                  <td>
                    {product.tags && product.tags.length > 0 ? (
                      product.tags.map((tag) => (
                        <span key={tag.id}>[{tag.name}] </span>
                      ))
                    ) : (
                      <span>None</span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
