import axios from 'axios';
import { useContext } from 'react';
import { LoadingContext } from './LoadingContext';

const useApiService = () => {
  const { setLoading } = useContext(LoadingContext);

  const axiosInstance = axios.create({
    baseURL: "http://127.0.0.1:5000/",
  });

  axiosInstance.interceptors.request.use(
    (config) => {
      setLoading(true);
      return config;
    },
    (error) => {
      setLoading(true);
      return Promise.reject(error);
    }
  );

  axiosInstance.interceptors.response.use(
    (response) => {
      setLoading(false);
      return response;
    },
    (error) => {
      setLoading(false);
      return Promise.reject(error);
    }
  );

  return {
    get: async (url) => {
      const response = await axiosInstance.get(url);
      return response.data;
    },
    post: async (url, data) => {
      const response = await axiosInstance.post(url, data);
      return response.data;
    },
  };
};

export default useApiService;